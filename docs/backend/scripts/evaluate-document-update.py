"""Parent-owned contract probes for the disposable backend-build trial.

Run with --project pointing to a copied fixture. Uses only that fixture's
in-memory SQLite factory; inspect modified code before running the probe.
The canonical deliberately defective fixture is expected to fail.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    sys.path.insert(0, str(project))
    database = load("trial_database", project / "database.py")
    service = load("trial_service", project / "service.py")
    cases = [
        ("empty object preserves", {}, 200, ("Original", "Original summary"), "doc-a"),
        ("summary-only preserves title", {"summary": "Changed"}, 200, ("Original", "Changed"), "doc-a"),
        ("summary null clears", {"summary": None}, 200, ("Original", None), "doc-a"),
        ("null title rejected", {"title": None}, 400, None, "doc-a"),
        ("empty title rejected", {"title": ""}, 400, None, "doc-a"),
        ("blank title rejected", {"title": " \t"}, 400, None, "doc-a"),
        ("numeric title rejected", {"title": 12}, 400, None, "doc-a"),
        ("boolean title rejected", {"title": True}, 400, None, "doc-a"),
        ("numeric summary rejected", {"title": "Valid", "summary": 12}, 400, None, "doc-a"),
        ("unknown field rejected", {"title": "Valid", "owner": "other"}, 400, None, "doc-a"),
        ("array payload rejected", [], 400, None, "doc-a"),
        ("null payload rejected", None, 400, None, "doc-a"),
        ("verbatim values retained", {"title": "  Kept  ", "summary": ""}, 200, ("  Kept  ", ""), "doc-a"),
        ("cross-tenant invalid payload hidden", None, 404, None, "doc-b"),
        ("missing invalid payload hidden", None, 404, None, "absent"),
        ("SQL-looking value remains data", {"title": "x'; DELETE FROM documents; --"}, 200,
         ("x'; DELETE FROM documents; --", "Original summary"), "doc-a"),
    ]
    results = []
    for name, payload, expected_status, expected_values, document_id in cases:
        connection = database.create_database()
        try:
            before = [tuple(row) for row in connection.execute("SELECT * FROM documents ORDER BY id")]
            status, body = service.patch_document(connection, "tenant-a", document_id, payload)
            assert status == expected_status, f"status {status}, expected {expected_status}"
            after = [tuple(row) for row in connection.execute("SELECT * FROM documents ORDER BY id")]
            if expected_status != 200:
                assert before == after, "rejected request changed records"
            else:
                assert body == dict(id=document_id, title=expected_values[0], summary=expected_values[1]), "response differs"
                assert after == [("doc-a", "tenant-a", *expected_values), before[1]], "persisted records differ"
            results.append({"case": name, "passed": True})
        except Exception as error:
            results.append({"case": name, "passed": False, "reason": type(error).__name__ + ": " + str(error)})
        finally:
            connection.close()
    passed = sum(result["passed"] for result in results)
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
