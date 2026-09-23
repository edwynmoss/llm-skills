"""Exercise package validation against deliberately damaged isolated libraries."""

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("checker", ROOT / "scripts/check-skill-library.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class LibraryTests(unittest.TestCase):
    def test_source_packages(self):
        for library in CHECKER.LIBRARIES:
            with self.subTest(library=library):
                self.assertEqual(CHECKER.audit(ROOT, library)["errors"], [])

    def test_detects_damage_and_preserves_library_isolation(self):
        for library, (prefix, _, _, decision_prefix) in CHECKER.LIBRARIES.items():
            other = "backend" if library == "ux" else "ux"
            rule = "GOV-99" if library == "ux" else "BGV-99"
            mutations = {
                "undefined rule": ("README.md", "\n" + rule, "Referenced rule has no canonical definition"),
                "missing link": ("README.md", "\n[Broken](absent-file.md)", "missing linked file"),
                "undefined decision": ("README.md", "\n" + decision_prefix + "99", "Referenced decision has no register entry"),
                "duplicate owner": ("governance.md", None, "Duplicate rule owner"),
                "malformed envelope": ("governance.md", "\n| " + rule + " | MUST | incomplete |", "expected six nonempty"),
                "missing entry": (None, None, "Missing entry skill"),
                "invalid metadata": (None, "\n---\nunknown: value\n---\n", "missing frontmatter delimiters"),
            }
            for name, (relative, addition, expected) in mutations.items():
                with self.subTest(library=library, damage=name), tempfile.TemporaryDirectory(prefix="skill-library-") as directory:
                    fixture = Path(directory)
                    shutil.copytree(ROOT / "docs", fixture / "docs")
                    shutil.copytree(ROOT / "skills", fixture / "skills")
                    shutil.copytree(ROOT / "scripts", fixture / "scripts")
                    for name in ("README.md", "VALIDATION.md"):
                        shutil.copy2(ROOT / name, fixture / name)
                    if relative:
                        target = fixture / "docs" / library / relative
                        if addition is None:
                            addition = "\n" + next(line for line in target.read_text(encoding="utf-8").splitlines() if line.startswith("| GOV-01 |") or line.startswith("| BGV-01 |"))
                        with target.open("a", encoding="utf-8") as stream:
                            stream.write(addition)
                    else:
                        target = fixture / "skills" / (prefix + "-build") / "SKILL.md"
                        if addition is None:
                            target.unlink()
                        else:
                            target.write_text(addition, encoding="utf-8")
                    errors = CHECKER.audit(fixture, library)["errors"]
                    self.assertTrue(any(expected in error for error in errors), errors)
                    self.assertEqual(CHECKER.audit(fixture, other)["errors"], [])


if __name__ == "__main__":
    unittest.main()
