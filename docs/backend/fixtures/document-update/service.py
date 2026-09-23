"""Request boundary in a deliberately defective evaluation fixture."""


def patch_document(connection, tenant_id, document_id, payload):
    row = connection.execute(
        "SELECT id, title, summary FROM documents WHERE tenant = ? AND id = ?",
        (tenant_id, document_id),
    ).fetchone()
    if row is None:
        return 404, {"error": "not_found"}

    title = payload.get("title")
    summary = payload.get("summary", row["summary"])
    with connection:
        connection.execute(
            "UPDATE documents SET title = ?, summary = ? WHERE tenant = ? AND id = ?",
            (title, summary, tenant_id, document_id),
        )
    return 200, {"id": row["id"], "title": title, "summary": summary}
