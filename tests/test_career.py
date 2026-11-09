"""Keep approved career content public, searchable, and distinct from code evidence."""
import json
import unittest
from pathlib import Path
from scripts.build_wiki import build, read_document

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('career', 'backend-experience', 'ai-experience', 'mentoring-experience')

class CareerTest(unittest.TestCase):
    def test_sources_are_self_reported_not_fabricated_code_evidence(self):
        for slug in PAGES:
            meta, body, _ = read_document(ROOT / f'docs/wiki/{slug}.md')
            self.assertEqual(meta['provenance'], 'self-reported')
            self.assertEqual(meta['sources'], [])
            self.assertIn('독립 검증 결과를 뜻하지 않습니다', body)
            self.assertIn('2026-11-09', body)

    def test_approved_employment_dates(self):
        text = (ROOT / 'docs/wiki/career.md').read_text()
        for value in ('메디플렉서스 | 2026.05 ~ 현재', '여기어때컴퍼니 | 2022.05 ~ 2026.04',
                      '지에스아이티엠 | 2022.01 ~ 2022.05', '케이웨더 | 2019.12 ~ 2021.12',
                      '유아이네트웍스 | 2018.11 ~ 2019.11'):
            self.assertIn(value, text)

    def test_pages_are_searchable_and_not_claimed_as_new_extraction(self):
        outputs = build(ROOT)
        search = json.loads(outputs['search-index.json'])
        knowledge = json.loads(outputs['knowledge.json'])
        for slug in PAGES:
            self.assertIn(f'wiki/{slug}.html', outputs)
            self.assertTrue(any(x['url'] == f'wiki/{slug}.html' for x in search))
            entity = next(x for x in knowledge['entities'] if x['id'] == slug)
            self.assertEqual(entity['provenance'], 'self-reported')
            self.assertIn('본인 제공·공개 확인', outputs[f'wiki/{slug}.html'])
        self.assertIn('신규 경력 문서 미포함', knowledge['analysis']['scope'])
