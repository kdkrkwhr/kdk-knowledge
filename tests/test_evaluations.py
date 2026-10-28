"""Keep the public repository reviews complete and distinct from guides."""

import json
import re
import unittest
from pathlib import Path

from scripts.build_wiki import read_document


ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = {
    "AgentRadio", "agent-drift-guard", "agent-hub", "airport-parking",
    "algorithms", "attendance-pwa", "auction-spot-front", "auction-spot",
    "dl-data-training", "dl-object-detecting", "dl-object-tracking",
    "dl-tesseract", "flask-leaflet", "flutter-profile", "hermes-agent-area",
    "hermes-agent", "hermes-env", "hermes-team-hub", "kdk-knowledge",
    "kdkrkwhr.github.com", "kdkrkwhr", "msa-architecture", "notebuddy",
    "resume", "spring-ai", "spring-boot", "spring-react-template", "standards",
}
CRITERIA = ("구조·설계", "구현 품질", "운영 준비", "유지보수")
RATINGS = "양호|보완 필요|위험|미확인"


class PublicEvaluationTest(unittest.TestCase):
    def test_every_repository_has_a_source_scoped_review(self):
        self.assertEqual(len(REPOSITORIES), 28)
        for slug in sorted(REPOSITORIES):
            with self.subTest(slug=slug):
                meta, body, _ = read_document(ROOT / "docs/wiki" / f"{slug}.md")
                self.assertEqual(meta["id"], slug)
                self.assertEqual(body.count("## 냉정한 기술 평가"), 1)
                section = body.split("## 냉정한 기술 평가\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn("**평가일:** 2026-10-28", section)
                self.assertRegex(section, r"\*\*근거 커밋:\*\* `[0-9a-f]{40}`")
                for criterion in CRITERIA:
                    self.assertRegex(section, rf"- \*\*{re.escape(criterion)} — ({RATINGS})\*\*")
                self.assertIn("**좋은 점:**", section)
                self.assertIn("**개선 우선순위:**", section)
                self.assertRegex(section, r"P[123]")
                self.assertIn("https://github.com/kdkrkwhr/", section)
                self.assertNotRegex(section, r"테스트|커버리지|test coverage")

    def test_reviews_are_published_and_searchable(self):
        index = json.loads((ROOT / "site/search-index.json").read_text(encoding="utf-8"))
        indexed = {entry["url"]: entry["body"] for entry in index}
        for slug in sorted(REPOSITORIES):
            with self.subTest(slug=slug):
                url = f"wiki/{slug}.html"
                self.assertIn("## 냉정한 기술 평가", indexed[url])
                page = (ROOT / "site" / url).read_text(encoding="utf-8")
                self.assertIn(">냉정한 기술 평가</h2>", page)


if __name__ == "__main__":
    unittest.main()
