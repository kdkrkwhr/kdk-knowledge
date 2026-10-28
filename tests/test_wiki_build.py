import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build_wiki import build


ROOT = Path(__file__).resolve().parents[1]


class WikiBuildTest(unittest.TestCase):
    def test_markdown_generates_readable_pages_search_and_relations(self):
        outputs = build(ROOT)
        self.assertIn("wiki/notebuddy.html", outputs)
        self.assertIn("wiki/auction-spot.html", outputs)
        self.assertIn("wiki/markdown/notebuddy.md", outputs)
        self.assertIn("상태 전이", outputs["wiki/notebuddy.html"])
        self.assertIn("로컬 디스크", outputs["wiki/auction-spot.html"])
        search = json.loads(outputs["search-index.json"])
        self.assertTrue(any(item["url"] == "wiki/notebuddy.html" for item in search))
        graph = json.loads(outputs["knowledge.json"])
        self.assertTrue(any(edge["from"] == "auction-spot" for edge in graph["relations"]))
        self.assertEqual(graph["analysis"]["status"], "run")
        self.assertIn("wiki/topics.html", outputs)
        self.assertIn("관련 개념", outputs["wiki/hermes-agent-area.html"])
        self.assertTrue(any(edge["origin"] == "extracted" and edge["score"] for edge in graph["relations"]))

    def test_document_navigation_marks_current_page_and_collapses_on_mobile(self):
        page = build(ROOT)["wiki/agent-hub.html"]
        self.assertIn('<details class="wiki-mobile-nav">', page)
        self.assertIn(f'문서 목록 · {len(list((ROOT / "docs/wiki").glob("*.md")))}개', page)
        self.assertEqual(page.count('href="agent-hub.html" aria-current="page"'), 2)

    def test_unregistered_public_source_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "docs/wiki", root / "docs/wiki")
            shutil.copytree(ROOT / "templates", root / "templates")
            page = root / "docs/wiki/notebuddy.md"
            page.write_text(page.read_text() + "\n[wrong](https://github.com/kdkrkwhr/notebook-pets/blob/main/README.md)\n")
            with self.assertRaisesRegex(ValueError, "unregistered source"):
                build(root)

    def test_broken_internal_document_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "docs/wiki", root / "docs/wiki")
            shutil.copytree(ROOT / "templates", root / "templates")
            page = root / "docs/wiki/notebuddy.md"
            page.write_text(page.read_text() + "\n[missing](missing.md)\n")
            with self.assertRaisesRegex(ValueError, "broken wiki link"):
                build(root)


if __name__ == "__main__":
    unittest.main()
