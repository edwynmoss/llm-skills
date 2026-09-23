import unittest
from database import create_database
from service import patch_document


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.connection = create_database()
        self.addCleanup(self.connection.close)

    def test_updates_title_and_summary(self):
        status, body = patch_document(self.connection, "tenant-a", "doc-a",
                                      {"title": "Revised", "summary": "Details"})
        self.assertEqual((status, body), (200, {"id": "doc-a", "title": "Revised", "summary": "Details"}))
        row = self.connection.execute("SELECT title, summary FROM documents WHERE id = 'doc-a'").fetchone()
        self.assertEqual(tuple(row), ("Revised", "Details"))

    def test_explicit_summary_clear(self):
        status, body = patch_document(self.connection, "tenant-a", "doc-a",
                                      {"title": "Revised", "summary": None})
        self.assertEqual(status, 200)
        self.assertIsNone(body["summary"])

    def test_cross_tenant_is_hidden_and_unchanged(self):
        self.assertEqual(patch_document(self.connection, "tenant-a", "doc-b", {"title": "Wrong"}),
                         (404, {"error": "not_found"}))
        self.assertEqual(self.connection.execute("SELECT title FROM documents WHERE id = 'doc-b'").fetchone()[0], "Other")

    def test_missing_is_hidden(self):
        self.assertEqual(patch_document(self.connection, "tenant-a", "absent", {"title": "New"}),
                         (404, {"error": "not_found"}))


if __name__ == "__main__":
    unittest.main()
