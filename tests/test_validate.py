import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import validate


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeValidationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "site", self.root / "site")

    def data(self):
        return json.loads((self.root / "site/knowledge.json").read_text())

    def save(self, data):
        (self.root / "site/knowledge.json").write_text(json.dumps(data))

    def test_public_snapshot_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_relation_needs_existing_evidence(self):
        data = self.data()
        data["relations"][0]["evidence"] = ["missing"]
        self.save(data)
        self.assertTrue(any("missing" in error for error in validate(self.root)))

    def test_source_must_be_public_and_pinned(self):
        data = self.data()
        source = data["sources"][0]
        source["visibility"] = "private"
        source["revision"] = "main"
        self.save(data)
        errors = validate(self.root)
        self.assertTrue(any("public" in error for error in errors))
        self.assertTrue(any("revision" in error for error in errors))

    def test_public_artifact_has_an_allowlist(self):
        (self.root / "site" / "notes.txt").write_text("not for publication")
        self.assertTrue(any("notes.txt" in error for error in validate(self.root)))

    def test_public_artifact_rejects_private_contact_or_local_path(self):
        path = self.root / "site/index.html"
        path.write_text(path.read_text() + "contact: private.person@example.test /Users/alice/notes")
        errors = validate(self.root)
        self.assertTrue(any("email" in error for error in errors))
        self.assertTrue(any("local path" in error for error in errors))

    def test_project_claim_link_must_be_in_source_register(self):
        path = self.root / "site/index.html"
        path.write_text(path.read_text() +
                        '<a href="https://github.com/kdkrkwhr/notebook-pets/blob/main/README.md">untracked</a>')
        self.assertTrue(any("Unregistered source link" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
