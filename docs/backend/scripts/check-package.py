"""Stable library-local entry to the shared structural validator."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("skill_library_check", Path(__file__).resolve().parents[3] / "scripts/check-skill-library.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def audit(root):
    return checker.audit(root, "backend")


if __name__ == "__main__":
    raise SystemExit(checker.main("backend"))
