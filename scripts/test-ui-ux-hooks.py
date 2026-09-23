"""Behavioural hook/installer checks using disposable, offline fixtures."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load("ui_ux_hooks", "ui-ux-hooks.py")
installer = load("install_ui_ux_hooks", "install-ui-ux-hooks.py")


class HooksTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ui-ux-hooks-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source with spaces"
        shutil.copytree(ROOT / "docs/ux", self.root / "docs/ux")
        for name in ("README.md", "VALIDATION.md"):
            shutil.copy2(ROOT / name, self.root / name)
        (self.root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/ui-ux-hooks.py", self.root / "scripts/ui-ux-hooks.py")
        shutil.copy2(ROOT / "scripts/check-skill-library.py", self.root / "scripts/check-skill-library.py")
        self.skills = self.base / "skills"
        for name in runtime.SKILLS:
            shutil.copytree(ROOT / "skills" / name, self.root / "skills" / name)
            shutil.copytree(ROOT / "skills" / name, self.skills / name)
            (self.skills / name / "library-root.txt").write_text(str(self.root / "docs/ux"), encoding="utf-8")
        self.codex = self.base / "codex"
        self.state = self.codex / "cache/ui-ux-hooks-state.json"
        self.environment = patch.dict(os.environ, {"UI_UX_DOCS_ROOT": str(self.root / "docs/ux")})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def invoke(self, name="PostToolUse", **fields):
        return runtime.handle({"hook_event_name": name, "session_id": "fixture", "tool_name": "apply_patch", **fields},
                              self.root, self.skills, self.state, os.environ)

    def message(self, result):
        return result["hookSpecificOutput"]["additionalContext"]

    def install(self, **options):
        return installer.install(self.root, self.skills, self.codex, **options)

    def test_health_and_no_application_requirement(self):
        self.assertIn("library available", self.message(self.invoke("SessionStart", cwd=str(self.base))))
        self.assertFalse(self.state.exists())

    def test_wrong_environment_does_not_fallback(self):
        os.environ["UI_UX_DOCS_ROOT"] = str(self.base / "missing")
        self.assertIn("NOT VERIFIED", self.message(self.invoke("SessionStart")))
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse(self.codex.exists())

    def test_locator_drift_and_entry_drift(self):
        locator = self.skills / "ui-spec/library-root.txt"
        locator.write_text(str(self.base), encoding="utf-8")
        self.assertIn("library-root.txt differs", self.message(self.invoke("SessionStart")))
        locator.write_text(str(self.root / "docs/ux"), encoding="utf-8")
        (self.skills / "ui-spec/SKILL.md").write_text("changed", encoding="utf-8")
        self.assertIn("SKILL.md differs", self.message(self.invoke("SessionStart")))

    def test_missing_reference_and_revision(self):
        governance = self.root / "docs/ux/governance.md"
        governance.unlink()
        self.assertIn("governance.md", self.message(self.invoke("SessionStart")))
        governance.write_text("No revision", encoding="utf-8")
        self.assertIn("no library revision", self.message(self.invoke("SessionStart")))

    def test_real_checker_pass_duplicate_and_unrelated_change(self):
        self.assertIn("VERIFIED:", self.message(self.invoke()))
        self.assertEqual(self.invoke(), {})
        (self.root / "application.txt").write_text("unrelated", encoding="utf-8")
        self.assertEqual(self.invoke(tool_name="Bash"), {})
        with (self.root / "docs/ux/README.md").open("a", encoding="utf-8") as stream:
            stream.write("\nAn intentional document change.\n")
        self.assertIn("VERIFIED:", self.message(self.invoke()))

    def test_shared_checker_change_invalidates_previous_success(self):
        self.assertIn("VERIFIED:", self.message(self.invoke()))
        self.assertEqual(self.invoke(), {})
        checker = self.root / "scripts/check-skill-library.py"
        original = checker.read_text(encoding="utf-8")
        checker.write_text("raise RuntimeError('controlled fixture failure')\n", encoding="utf-8")
        self.assertIn("NOT VERIFIED", self.message(self.invoke()))
        checker.write_text(original + "\n# Reviewed checker revision.\n", encoding="utf-8")
        self.assertIn("VERIFIED:", self.message(self.invoke()))

    def test_missing_linked_root_document_invalidates_previous_success(self):
        self.assertIn("VERIFIED:", self.message(self.invoke()))
        self.assertEqual(self.invoke(), {})
        document = self.root / "VALIDATION.md"
        original = document.read_bytes()
        document.unlink()
        self.assertIn("NOT VERIFIED", self.message(self.invoke()))
        document.write_bytes(original)
        # Previously verified bytes are valid again after restoration.
        self.assertEqual(self.invoke(), {})

    def test_real_failure_repair_and_new_session(self):
        readme = self.root / "docs/ux/README.md"
        original = readme.read_text(encoding="utf-8")
        readme.write_text(original + "\n[Broken reference](absent-document.md)\n", encoding="utf-8")
        result = self.invoke()
        self.assertIn("FAILED:", self.message(result))
        self.assertIn("absent-document.md", self.message(result))
        self.assertNotIn("decision", result)
        self.assertEqual(self.invoke(), {})
        self.assertIn("FAILED:", self.message(self.invoke(session_id="second")))
        readme.write_text(original, encoding="utf-8")
        self.assertIn("VERIFIED:", self.message(self.invoke()))

    def test_out_of_scope_and_missing_session(self):
        self.assertEqual(self.invoke("Stop"), {})
        self.assertEqual(self.invoke(tool_name="WebSearch"), {})
        self.assertFalse(self.state.exists())
        self.assertIn("NOT VERIFIED", self.message(self.invoke(session_id=None)))

    def test_timeout_invalid_output_and_cache_retry(self):
        for effect in (subprocess.TimeoutExpired("checker", 5), ValueError("Invalid report")):
            with self.subTest(effect=type(effect).__name__), patch.object(runtime, "check_package", side_effect=effect):
                self.assertIn("NOT VERIFIED", self.message(self.invoke()))
                self.assertFalse(self.state.exists())
        self.assertIn("VERIFIED:", self.message(self.invoke()))

    def test_real_checker_crash_is_not_a_pass(self):
        (self.root / "docs/ux/scripts/check-package.py").write_text("raise RuntimeError('private diagnostic')", encoding="utf-8")
        message = self.message(self.invoke())
        self.assertIn("NOT VERIFIED", message)
        self.assertNotIn("private diagnostic", message)

    def test_changed_during_check_is_not_cached(self):
        def change(_root):
            (self.root / "docs/ux/race.md").write_text("changed", encoding="utf-8")
            return "VERIFIED"
        with patch.object(runtime, "check_package", side_effect=change):
            self.assertIn("changed during validation", self.message(self.invoke()))
        self.assertFalse(self.state.exists())

    def test_cache_lock_conflict_does_not_report_pass(self):
        with runtime.state_lock(self.state):
            self.assertIn("NOT VERIFIED", self.message(self.invoke()))
        self.assertIn("VERIFIED:", self.message(self.invoke()))

    def test_bounded_cache_and_no_event_data_stored(self):
        self.state.parent.mkdir(parents=True)
        runtime.write_state(self.state, {str(i): "fingerprint" for i in range(40)})
        self.assertEqual(len(runtime.read_state(self.state)), 32)
        self.invoke(tool_input={"command": "DO NOT EXECUTE OR STORE"}, transcript_path="DO NOT READ")
        content = self.state.read_text()
        self.assertNotIn("DO NOT", content)
        self.assertNotIn("fixture", content)

    def test_corrupt_cache_and_large_source_are_not_verified(self):
        self.state.parent.mkdir(parents=True)
        self.state.write_text("broken", encoding="utf-8")
        self.assertIn("NOT VERIFIED", self.message(self.invoke()))
        self.state.unlink()
        (self.root / "docs/ux/large.md").write_bytes(b"x" * (runtime.INPUT_LIMIT + 1))
        self.assertIn("byte budget", self.message(self.invoke()))

    def test_cli_invalid_event_is_json_and_bounded(self):
        command = [sys.executable, "-I", "-B", str(self.root / "scripts/ui-ux-hooks.py"),
                   "--root", str(self.root), "--skills-dir", str(self.skills), "--state", str(self.state)]
        for data in ("[]", "{", "x" * (runtime.INPUT_LIMIT + 1)):
            result = subprocess.run(command, input=data, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0)
            self.assertIn("NOT VERIFIED", json.loads(result.stdout)["systemMessage"])
            self.assertEqual(result.stderr, "")

    def test_dry_run_install_repeat_and_remove(self):
        self.assertEqual(self.install(dry_run=True)["changed_files"], 2)
        self.assertFalse(self.codex.exists())
        self.assertEqual(self.install()["changed_files"], 2)
        self.assertEqual(self.install()["changed_files"], 0)
        self.assertEqual(self.install(remove=True)["changed_files"], 2)
        self.assertFalse((self.codex / "hooks.json").exists())
        self.assertEqual(self.install(remove=True)["changed_files"], 0)

    def test_preserve_unrelated_hooks_config_and_remove(self):
        self.codex.mkdir()
        unrelated = {"description": "Keep me", "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "existing"}]}]}}
        path = self.codex / "hooks.json"
        path.write_text(json.dumps(unrelated), encoding="utf-8")
        config = self.codex / "config.toml"
        config.write_text("# keep formatting\nmodel = 'existing'\n", encoding="utf-8")
        before = config.read_bytes()
        self.install()
        self.assertEqual(json.loads(path.read_text())["hooks"]["Stop"], unrelated["hooks"]["Stop"])
        self.install(remove=True)
        self.assertEqual(json.loads(path.read_text()), unrelated)
        self.assertEqual(config.read_bytes(), before)

    def test_edited_hook_and_invalid_configuration_preserved(self):
        self.install()
        path = self.codex / "hooks.json"
        changed = path.read_text().replace("UI/UX library health", "User edit")
        path.write_text(changed, encoding="utf-8")
        for options in ({}, {"update": True}, {"remove": True}):
            with self.assertRaises(ValueError):
                self.install(**options)
            self.assertEqual(path.read_text(), changed)
        path.write_text("not json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(path.read_text(), "not json")

    def test_disabled_and_inline_hooks_are_preserved(self):
        self.codex.mkdir()
        config = self.codex / "config.toml"
        for content in ("[features]\nhooks = false\n", "[hooks]\nSessionStart = []\n"):
            config.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                self.install()
            self.assertFalse((self.codex / "hooks.json").exists())
            self.assertEqual(config.read_text(), content)

    def test_partial_write_failure_rolls_back(self):
        actual = installer.atomic_write
        def fail_manifest(path, content):
            if path.name == installer.MANIFEST:
                raise OSError("simulated write failure")
            actual(path, content)
        with patch.object(installer, "atomic_write", side_effect=fail_manifest), self.assertRaises(OSError):
            self.install()
        self.assertFalse(self.codex.exists())

    def test_codex_trust_state_does_not_conflict_with_json_hooks(self):
        self.install()
        config = self.codex / "config.toml"
        content = '[hooks.state."fixture-key"]\ntrusted_hash = "sha256:fixture"\n'
        config.write_text(content, encoding="utf-8")
        self.assertEqual(self.install()["changed_files"], 0)
        self.assertEqual(config.read_text(), content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
