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
        for path in (SITE / "index.html", SITE / "architecture/index.html"):
            with self.subTest(path=path):
                parser = PageParser()
                parser.feed(path.read_text(encoding="utf-8"))
                self.assertEqual(set(parser.fragments) - parser.ids, set())

    def test_extraction_is_labelled_separately_from_curated_relations(self):
        wiki = (SITE / "index.html").read_text(encoding="utf-8")
        map_page = (SITE / "architecture/index.html").read_text(encoding="utf-8")
        self.assertIn("LLM이 공개 소스를 읽고 대조해 작성", wiki)
        self.assertIn("Graphify 분석 실행", map_page)
        self.assertIn("편집 관계", map_page)
        self.assertIn("자동 추출", map_page)
        data = json.loads((SITE / "knowledge.json").read_text(encoding="utf-8"))
        self.assertEqual(data["analysis"]["status"], "run")
        self.assertTrue(any(relation["origin"] == "extracted" for relation in data["relations"]))
        self.assertTrue(any(relation["origin"] == "curated" for relation in data["relations"]))

    def test_project_stories_are_the_primary_navigation(self):
        page = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="#notebuddy"', page)
        self.assertIn('href="#auction-spot"', page)
        self.assertIn('id="notebuddy"', page)
        self.assertIn('id="auction-spot"', page)
        self.assertIn('id="career"', page)
        self.assertNotIn('class="sidebar"', page)
        self.assertNotIn('class="outline"', page)

    def test_stories_use_pinned_source_files_without_requiring_other_wikis(self):
        page = (SITE / "index.html").read_text(encoding="utf-8")
        data = json.loads((SITE / "knowledge.json").read_text(encoding="utf-8"))
        self.assertIn("LocalImageStorageService.java", page)
        self.assertIn("game_api.py", page)
        self.assertNotIn("notebook-pets/wiki/", page)
        self.assertTrue(any(source["repository"] == "kdkrkwhr/auction-spot-api"
                            and source["path"].endswith(".java") for source in data["sources"]))
        self.assertTrue(any(entity["id"] == "auction-spot" for entity in data["entities"]))

    def test_dark_project_theme(self):
        css = (SITE / "style.css").read_text(encoding="utf-8")
        self.assertIn("color-scheme:dark", css)
        self.assertIn(".project-ledger", css)

    def test_search_and_map_refresh_generated_data(self):
        for path in (SITE / "wiki.js", SITE / "architecture/map.js"):
            with self.subTest(path=path):
                self.assertIn("cache: 'no-store'", path.read_text(encoding="utf-8"))
        self.assertNotIn("wiki.js", (SITE / "index.html").read_text(encoding="utf-8"))

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
