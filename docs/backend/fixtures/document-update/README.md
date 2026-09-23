# Partial document update evaluation fixture

This is a deliberately incomplete fictional project used to test backend-build. It is not recommended application code. Use Python 3.11+ standard library; there are no dependencies or servers. `service.py` is the existing request-handler boundary and `database.py` owns persistence setup. Tests use fresh in-memory SQLite instances and close them.

User request: repair partial document updates using the existing architecture. An omitted title or summary must preserve the current value. Explicit null summary clears it. Explicit null, non-string or blank title is invalid. Summary must be a string or null. Unknown fields must be rejected. An empty object is a valid no-op. Successful values are preserved exactly; no trimming or normalization was requested.

The caller supplies an already-authenticated trusted tenant ID. The existing tenant-scoped lookup must continue to hide a different tenant's or missing document using status 404. This check precedes field-error disclosure. Invalid payloads produce 400 without any row change. A valid update returns 200 with id, title and summary matching the persisted row. The payload must be a JSON object represented as a Python dict.

Make the smallest maintainable fix and add meaningful tests. Do not alter the schema, introduce a framework, replace the data access layer or install packages. Run `python -B -m unittest -v` in the copied fixture. Do not weaken or remove existing tests. Only edit the disposable copy supplied by the evaluator.
