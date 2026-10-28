---
{"id":"kdk-knowledge","type":"project","order":78,"mapTitle":"중앙 지식 허브 구현","summary":"공개 원본 커밋을 Markdown 문서·검색·관계 지도로 빌드하는 저장소","sources":["kdk-knowledge-1","kdk-knowledge-2","kdk-knowledge-3"],"relations":[{"to":"standards","label":"개발 기준을 한 참고 자료로 문서화","evidence":["kdk-knowledge-1"]}]}
---
# 중앙 지식 허브 구현

**분석 기준:** `300e554c442c86522e121f7b17dd3ba738fcacd4`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `300e554c442c86522e121f7b17dd3ba738fcacd4`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** Markdown 원본에서 HTML·검색 색인·관계 데이터를 함께 만들어 서로 다른 화면의 내용 기준을 맞춘다. [build_wiki.py의 build, 121–183행](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/build_wiki.py)
- **구현 품질 — 보완 필요** 간단한 Markdown 파서는 제목·평면 목록·링크·코드만 처리한다. 중첩 목록이나 표를 추가하면 구조가 예상과 다르게 평문 처리될 수 있다. 현재 문서의 지원 구문은 README에 명시돼 있다. [build_wiki.py의 render_markdown, 54–118행](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/build_wiki.py)
- **운영 준비 — 양호** 공개 산출물 범위를 제한하고 등록 근거의 커밋·경로·공개 여부를 검사하는 경계가 있다. 이는 서술의 의미적 정확성까지 보증하지는 않는다. [validate.py 18–69행](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/validate.py)
- **유지보수 — 보완 필요** 근거 ID·본문 링크·관계는 사람이 같이 갱신해야 하므로 원본 변경 후 문장 대조를 놓칠 수 있다. 자동 생성은 편집의 대체가 아니다. [README.md 16–24행](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/README.md)

**좋은 점:** 출처 고정과 사람의 해설을 분리한 구조가 명확하다. **개선 우선순위:** P2 — 지원하지 않는 Markdown 구조를 빌드에서 명확히 거부하고, 원본 커밋 변경 시 문장 대조 항목을 기록하면 조용한 표시 오류와 낡은 설명을 줄인다.

## 편집 원본과 생성물

README는 `docs/wiki/*.md`를 사람이 읽고 수정하는 원본으로 지정한다. `scripts/build_wiki.py`가 front matter와 본문을 읽어 정적 HTML·Markdown 원본 복사·검색 인덱스·관계 JSON을 생성한다. 현재 문서와 지도는 원본 저장소의 동작에 대한 사람이 쓴 설명이며 원본 저장소를 자동 변경하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/README.md) [원본: `scripts/build_wiki.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/build_wiki.py)

## 검증 경계

`scripts/validate.py`는 등록된 근거 URL의 저장소·커밋·경로 일치, 공개 여부, 문서 링크와 관계 근거를 검사한다. 이 검사는 원본 코드 실행이나 진술의 의미적 진실 전체를 자동 판정하지 않는다. 관계는 편집 데이터이며 Graphify 추출은 아직 수행하지 않았다.
[원본: `scripts/validate.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/validate.py) [원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/README.md)

## 버전 기준

이 문서는 평가 작성 직전 공개된 고정 커밋을 근거로 한다. 이후 문서가 늘어나더라도 이 커밋의 구현 설명과 현재 사이트 산출물은 별도 시점일 수 있다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/README.md) [원본: `scripts/build_wiki.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/300e554c442c86522e121f7b17dd3ba738fcacd4/scripts/build_wiki.py)

## 연결해서 읽기

[문서 갱신 절차](maintenance.md)가 새로운 근거를 등록하는 방법을, [공개 저장소 목록](repositories.md)이 범위를 설명한다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
