"""Release-boundary regression checks with synthetic, disposable inputs."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_check", ROOT / "scripts/check-release.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        fixture = tempfile.TemporaryDirectory(prefix="skill-release-")
        self.addCleanup(fixture.cleanup)
        self.root = Path(fixture.name)
        (self.root / "README.md").write_text("# Public fixture\n", encoding="utf-8")
        self.inventory = {"files": ["README.md", "release-files.json"],
                          "allowed_url_hosts": ["example.invalid"]}
        self.save_inventory()

    def save_inventory(self):
        (self.root / "release-files.json").write_text(json.dumps(self.inventory), encoding="utf-8")

    def errors(self):
        return CHECKER.audit(self.root)["errors"]

    def test_real_package_and_clean_control(self):
        self.assertEqual(CHECKER.audit(ROOT)["errors"], [])
        self.assertEqual(self.errors(), [])

    def test_unreviewed_and_missing_files(self):
        extra = self.root / "environment.txt"
        extra.write_text("synthetic", encoding="utf-8")
        self.assertTrue(any("unreviewed file" in error for error in self.errors()))
        extra.unlink()
        (self.root / "README.md").unlink()
        self.assertTrue(any("missing file" in error for error in self.errors()))

    def test_detects_synthetic_sensitive_values_without_echoing_them(self):
        samples = ["ghp_" + "x" * 36, "-----BEGIN " + "PRIVATE KEY-----",
                   "C:/" + "Users/" + "fixture-person/private.txt",
                   "/home/" + "fixture-person/private.txt",
                   "fixture-person" + "@example.invalid"]
        for value in samples:
            with self.subTest(kind=value[:3]):
                (self.root / "README.md").write_text(value, encoding="utf-8")
                errors = self.errors()
                self.assertTrue(errors)
                self.assertNotIn(value, "\n".join(errors))

    def test_unreviewed_url_and_positive_public_reference(self):
        for scheme in ("https://", "HTTPS://", "HtTpS://"):
            with self.subTest(scheme=scheme):
                (self.root / "README.md").write_text("[Outside](" + scheme + "unreviewed.invalid/page)", encoding="utf-8")
                self.assertTrue(any("URL host" in error for error in self.errors()))
        (self.root / "README.md").write_text("[Source](https://example.invalid/page)", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_external_link_and_inventory_traversal(self):
        (self.root / "README.md").write_text("[Outside](../outside.md)", encoding="utf-8")
        self.assertTrue(any("external local link" in error for error in self.errors()))
        self.inventory["files"].append("../outside.md")
        self.save_inventory()
        self.assertIn("Invalid inventory path", self.errors())

    def test_duplicate_inventory(self):
        self.inventory["files"].append("README.md")
        self.save_inventory()
        self.assertIn("Duplicate inventory path", self.errors())


if __name__ == "__main__":
    unittest.main()
