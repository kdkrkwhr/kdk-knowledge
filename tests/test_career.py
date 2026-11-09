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

    def test_expanded_experience_scope_and_boundaries(self):
        outputs = build(ROOT)
        expectations = {
            'backend-experience': ('기존 계약을 유지하는 서비스 전환', '사용자 알림과 이벤트 처리', 'IoT와 실시간 관제'),
            'ai-experience': ('Dense·sparse 검색과 저장소 전환', 'LoRA 학습과 추론 서빙', '일치율은 전체 AI 서비스의 정확도와 다릅니다'),
            'mentoring-experience': ('백엔드: 동시 요청', 'AI: 생성 결과', 'AGENTS.md', '교육생이 모든 제안을 구현했다거나'),
            'career': ('업무 경험의 흐름', '프로젝트 밖에서 경험을 공유하는 방식'),
        }
        for slug, fragments in expectations.items():
            for fragment in fragments:
                self.assertIn(fragment, outputs[f'wiki/{slug}.html'])
        self.assertIn('실무 RAG·모델 서빙 경험을 교육생 프로젝트에서 그대로 수행한 것처럼 연결하지 않습니다', outputs['wiki/ai-experience.html'])

    def test_hereotta_operating_experience_keeps_scope_explicit(self):
        outputs = build(ROOT)
        page = outputs['wiki/backend-experience.html']
        for fragment in ('Kafka: 메시지 전달과 업무 처리의 차이',
                         'MSA: 서비스 경계와 변경 영향 이해하기',
                         '안정적인 운영을 위한 인프라와 배포 작업',
                         '전체 플랫폼 인프라를 단독 설계·운영했다는 뜻이 아니며'):
            self.assertIn(fragment, page)
        self.assertIn('Kafka·MSA', outputs['wiki/career.html'])
