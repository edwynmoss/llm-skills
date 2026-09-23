"""Check the reviewed publication inventory and detectable disclosure risks.

Standard-library only. This is a bounded release check, not a confidentiality
certification. Review prose, source history and Git identity before publishing.
"""

import argparse
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
URL = re.compile(r"https?://[^\s<>\(\)\]\"']+", re.IGNORECASE)
PATTERNS = {
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b",
    "signed token": r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b",
    "webhook credential": r"https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]{30,}",
    "personal path": r"(?:[A-Za-z]:[/\\]Users[/\\][^\s/\\]+|/(?:Users|home)/[^\s/]+/)",
    "email address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
}


def audit(root):
    root = root.resolve()
    errors = []
    manifest = json.loads((root / "release-files.json").read_text(encoding="utf-8"))
    expected = manifest["files"]
    hosts = set(manifest["allowed_url_hosts"])
    if len(expected) != len(set(expected)):
        errors.append("Duplicate inventory path")
    if "release-files.json" not in expected:
        errors.append("Inventory must include itself")
    for name in expected:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
            errors.append("Invalid inventory path")
    if errors:
        return {"status": "FAILED", "files": 0, "errors": errors}

    actual = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[0] == ".git":
            continue
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            errors.append(f"{relative.as_posix()}: linked filesystem input")
        elif path.is_file():
            actual.add(relative.as_posix())
    for name in sorted(actual - set(expected)):
        errors.append(f"{name}: unreviewed file")
    for name in sorted(set(expected) - actual):
        errors.append(f"{name}: missing file")

    for name in sorted(actual & set(expected)):
        path = root / name
        if not path.resolve().is_relative_to(root):
            errors.append(f"{name}: external file")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{name}: non-UTF-8 input requires review")
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, content):
                errors.append(f"{name}: possible {label}")
        for url in URL.findall(content):
            try:
                parsed = urlsplit(url)
                if parsed.hostname not in hosts or parsed.username or parsed.password:
                    errors.append(f"{name}: unreviewed URL host or embedded credentials")
            except ValueError:
                errors.append(f"{name}: malformed URL")
        if path.suffix.lower() == ".md":
            for target in LINK.findall(content):
                if target.startswith("#"):
                    continue
                try:
                    parsed = urlsplit(target)
                except ValueError:
                    errors.append(f"{name}: malformed Markdown link")
                    continue
                if parsed.scheme:
                    if parsed.scheme not in {"http", "https"}:
                        errors.append(f"{name}: unsupported link scheme")
                    elif parsed.hostname not in hosts or parsed.username or parsed.password:
                        errors.append(f"{name}: unreviewed Markdown URL host or embedded credentials")
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                if not resolved.is_relative_to(root) or not resolved.is_file():
                    errors.append(f"{name}: missing or external local link")
    return {"status": "FAILED" if errors else "VERIFIED", "files": len(actual),
            "scope": "Reviewed inventory, links and recognizable disclosure patterns only",
            "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    arguments = parser.parse_args()
    result = audit(arguments.root)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))
