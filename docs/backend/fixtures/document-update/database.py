"""Disposable in-memory persistence for the skill evaluation fixture."""
import sqlite3


def create_database():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE documents (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, "
        "title TEXT NOT NULL, summary TEXT)"
    )
    connection.executemany(
        "INSERT INTO documents VALUES (?, ?, ?, ?)",
        [("doc-a", "tenant-a", "Original", "Original summary"),
         ("doc-b", "tenant-b", "Other", "Other summary")],
    )
    connection.commit()
    return connection
