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

    def test_extraction_is_not_claimed(self):
        wiki = (SITE / "index.html").read_text(encoding="utf-8")
        map_page = (SITE / "architecture/index.html").read_text(encoding="utf-8")
        self.assertIn("LLM이 공개 소스를 읽고 대조해 작성", wiki)
        self.assertIn("Graphify 분석 미실행", map_page)
        self.assertIn("편집 관계", map_page)

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


if __name__ == "__main__":
    unittest.main()
