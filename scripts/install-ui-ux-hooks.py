"""Install/remove only the two UI/UX hooks. Python 3.11+, no dependencies.

Preserves unrelated hooks and config.toml. Codex trust review is a separate step.
"""

import argparse
import copy
import importlib.util
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "ui-ux-hooks-install.json"


def definitions(root, skills, codex):
    arguments = [str(Path(sys.executable).resolve()), "-I", "-B", str(root / "scripts/ui-ux-hooks.py"),
                 "--root", str(root), "--skills-dir", str(skills),
                 "--state", str(codex / "cache/ui-ux-hooks-state.json")]
    windows = "& " + " ".join("'" + value.replace("'", "''") + "'" for value in arguments)
    common = {"type": "command", "command": shlex.join(arguments), "commandWindows": windows,
              "timeout": 10, "additionalContextLimit": 1200}
    return {
        "SessionStart": {"matcher": "^(startup|resume|clear|compact)$", "hooks": [
            {**common, "statusMessage": "UI/UX library health"}]},
        "PostToolUse": {"matcher": "^(Bash|apply_patch|Edit|Write)$", "hooks": [
            {**common, "statusMessage": "UI/UX package integrity"}]},
    }


def read_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def merge_hooks(document, previous, desired):
    """Own exact groups recorded at installation; never adopt an ambiguous match."""
    result = copy.deepcopy(document)
    if not isinstance(result, dict) or not isinstance(result.get("hooks", {}), dict):
        raise ValueError("Existing hooks.json is not a hooks object; preserved")
    events = result.setdefault("hooks", {})
    for event, group in previous.items():
        groups = events.get(event, [])
        if not isinstance(groups, list) or groups.count(group) != 1:
            raise ValueError("Previously installed UI/UX hook was edited or duplicated; reconcile it before updating")
        groups.remove(group)
        if not groups:
            events.pop(event, None)
    # Do not introduce duplicate copies or take over somebody else's edited handler.
    if "ui-ux-hooks.py" in json.dumps(events):
        raise ValueError("Unmanaged UI/UX hook already exists; reconcile duplicate configuration")
    for event, group in desired.items():
        if not isinstance(events.get(event, []), list):
            raise ValueError(f"Invalid existing {event} hook groups; preserved")
        events.setdefault(event, []).append(group)
    return result


def atomic_write(path, content):
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".ui-ux-install-")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def install(root, skills, codex, *, dry_run=False, remove=False, update=False):
    hook_path = codex / "hooks.json"
    manifest_path = codex / MANIFEST
    if hook_path.is_symlink() or manifest_path.is_symlink():
        raise ValueError("Symlink configuration target; no files changed")
    original = {p: p.read_bytes() if p.exists() else None for p in (hook_path, manifest_path)}
    document = read_json(hook_path, {})
    manifest = read_json(manifest_path, {})
    previous = manifest.get("definitions", {})
    if manifest and (manifest.get("version") != 1 or not isinstance(previous, dict) or not previous):
        raise ValueError("Unrecognized UI/UX installation manifest; preserved")
    if not remove:
        config_path = codex / "config.toml"
        config = tomllib.loads(config_path.read_text(encoding="utf-8-sig")) if config_path.exists() else {}
        if config.get("features", {}).get("hooks") is False or config.get("features", {}).get("codex_hooks") is False:
            raise ValueError("Codex hooks are disabled; config.toml preserved")
        # Codex stores trust decisions under hooks.state; that is not an inline handler.
        hook_config = config.get("hooks", {})
        if any(key not in {"state", "managed_dir", "windows_managed_dir"} for key in hook_config):
            raise ValueError("Inline user hooks already exist; choose one representation before installation")
        spec = importlib.util.spec_from_file_location("ui_ux_hooks", root / "scripts/ui-ux-hooks.py")
        runtime = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runtime)
        runtime.library_health(root, skills, os.environ)
        desired = definitions(root, skills, codex)
        if previous and previous != desired and not update:
            raise ValueError("UI/UX hook definitions changed; review and use --update")
    else:
        desired = {}
        if not previous:
            return {"changed_files": 0, "removed": True, "dry_run": dry_run}
    result = merge_hooks(document, previous, desired)
    manifest_result = {"version": 1, "definitions": desired, "created_hooks_file": manifest.get("created_hooks_file", original[hook_path] is None)}
    hook_bytes = (json.dumps(result, indent=2, ensure_ascii=True) + "\n").encode()
    # Preserve exact bytes when the semantic configuration is already correct.
    if result == document:
        hook_bytes = original[hook_path]
    if remove and manifest.get("created_hooks_file") and result == {"hooks": {}}:
        hook_bytes = None
    manifest_bytes = None if remove else (json.dumps(manifest_result, indent=2) + "\n").encode()
    changes = {p: content for p, content in ((hook_path, hook_bytes), (manifest_path, manifest_bytes)) if content != original[p]}
    if not dry_run and changes:
        created_directory = not codex.exists()
        codex.mkdir(parents=True, exist_ok=True)
        applied = []
        try:
            for path, content in changes.items():
                # Do not overwrite a concurrent configuration edit.
                if (path.read_bytes() if path.exists() else None) != original[path]:
                    raise ValueError("Configuration changed during installation; retry after review")
                if content is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, content)
                applied.append(path)
        except Exception:
            for path in reversed(applied):
                if original[path] is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, original[path])
            if created_directory and not any(codex.iterdir()):
                codex.rmdir()
            raise
    return {"changed_files": len(changes), "removed": remove, "dry_run": dry_run,
            "hooks_file": str(hook_path), "config_toml_changed": False,
            "trust": "Review the two definitions in Codex /hooks; installation does not grant trust."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-dir", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--remove", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()
    try:
        result = install(ROOT, args.skills_dir.resolve(), args.codex_dir.resolve(),
                         dry_run=args.dry_run, remove=args.remove, update=args.update)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
