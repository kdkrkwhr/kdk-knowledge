import unittest
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
        self.assertIn("LLM 작성 · 공개 소스 대조", wiki)
        self.assertIn("Graphify 분석 미실행", map_page)
        self.assertIn("편집 관계", map_page)


if __name__ == "__main__":
    unittest.main()
