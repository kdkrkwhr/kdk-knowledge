import unittest
import json
from html.parser import HTMLParser
from pathlib import Path


SITE = Path(__file__).resolve().parents[1] / "site"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])


class SiteTest(unittest.TestCase):
    def test_in_page_links_have_targets(self):
        for path in (SITE / "index.html", SITE / "wiki/hermes-agent-area.html"):
            with self.subTest(path=path):
                parser = PageParser()
                parser.feed(path.read_text(encoding="utf-8"))
                self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_two_surfaces_wiki_index_and_graph(self):
        index = (SITE / "index.html").read_text(encoding="utf-8")
        graph = (SITE / "graph/index.html").read_text(encoding="utf-8")
        self.assertIn('class="hero"', index)
        self.assertIn('href="wiki/notebuddy.html"', index)
        self.assertIn('href="./graph/"', index)
        self.assertNotIn("architecture/", index)
        self.assertIn("위키 열기", graph)
        self.assertIn("kg-modal", graph)
        self.assertIn('href="../"', graph)

    def test_extraction_is_labelled_separately_from_curated_relations(self):
        index = (SITE / "index.html").read_text(encoding="utf-8")
        page = (SITE / "wiki/hermes-agent-area.html").read_text(encoding="utf-8")
        self.assertIn("자동 추출", index)
        self.assertIn("사람이 대조", page)
        self.assertIn("관련 개념", page)
        data = json.loads((SITE / "knowledge.json").read_text(encoding="utf-8"))
        self.assertEqual(data["analysis"]["status"], "run")
        self.assertTrue(any(relation["origin"] == "extracted" for relation in data["relations"]))
        self.assertTrue(any(relation["origin"] == "curated" for relation in data["relations"]))

    def test_documents_group_by_graph_topic(self):
        page = (SITE / "wiki/hermes-agent-area.html").read_text(encoding="utf-8")
        self.assertIn("<details><summary>", page)
        self.assertIn('class="tag">', page)
        self.assertIn('class="srcs"', page)
        self.assertIn("커밋 e3e118f", page)

    def test_theme_follows_system_and_keeps_korean_words(self):
        css = (SITE / "style.css").read_text(encoding="utf-8")
        self.assertIn("color-scheme:light dark", css)
        self.assertIn("prefers-color-scheme:dark", css)
        self.assertIn("word-break:keep-all", css)

    def test_search_refreshes_generated_data(self):
        self.assertIn("cache: 'no-store'", (SITE / "wiki.js").read_text(encoding="utf-8"))

    def test_public_repository_inventory_has_source_backed_pages(self):
        data = json.loads((SITE / "knowledge.json").read_text(encoding="utf-8"))
        repositories = {source["repository"].split("/", 1)[1]
                        for source in data["sources"] if source["repository"].startswith("kdkrkwhr/")}
        expected = {
            "notebook-pets", "auction-spot-api", "agent-hub", "auction-spot-front",
            "hermes-env", "hermes-agent-area", "hermes-team-hub", "agent-drift-guard",
            "engineering-standards", "attendance-pwa", "msa-architecture", "spring-boot",
            "spring-react-template", "airport-parking", "flask-leaflet", "flutter-profile",
            "dl-object-tracking", "dl-object-detecting", "dl-data-training", "dl-tesseract",
            "algorithms", "kdkrkwhr.github.com", "resume", "kdkrkwhr", "kdk-knowledge",
            "spring-ai", "hermes-agent", "AgentRadio",
        }
        self.assertEqual(repositories, expected)
        for repo in expected - {"notebook-pets", "auction-spot-api", "agent-hub", "engineering-standards"}:
            with self.subTest(repo=repo):
                self.assertTrue((SITE / "wiki" / f"{repo}.html").is_file())
        for repo in ("spring-ai", "hermes-agent", "AgentRadio"):
            entity = next(entity for entity in data["entities"] if entity["id"] == repo)
            self.assertEqual(entity["type"], "reference")


if __name__ == "__main__":
    unittest.main()
