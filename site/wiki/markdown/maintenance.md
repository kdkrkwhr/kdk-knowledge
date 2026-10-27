---
{"id":"maintenance","type":"guide","order":70,"summary":"공개 원본을 읽어 문서·근거·관계를 갱신하는 절차","sources":[],"relations":[]}
---
# 문서 작성과 갱신

이 위키의 편집 원본은 `docs/wiki/*.md`다. HTML, 검색 데이터, 관계 JSON은 빌드 산출물이다. 원본 프로젝트의 위키는 필수가 아니다. README뿐 아니라 구현 코드·설정·의존성·테스트·문서의 **구체적 파일과 고정 커밋**을 읽고 이곳에서 설명한다. 테스트 파일의 존재와 테스트 실행 성공은 별개의 주장이다.

## 한 프로젝트를 추가할 때

1. [저장소 목록](repositories.md)에서 대상을 고른다. fork·템플릿·보관 자료인지 README와 코드를 확인한다. 저장소 소유만으로 단독 저작이나 개인 역할을 주장하지 않는다.
2. 공개할 수 있는 파일 URL을 전체 커밋 SHA로 고정하고 `docs/wiki/sources.json`에 등록한다. 공개 범위가 불확실한 경력·성과·개인정보는 등록하지 않는다.
3. 프로젝트 Markdown에 개요, 해결 대상, 실제 구조, 주요 실행·데이터 흐름, 사용 기술, 확인 범위와 미확인 사항을 쓴다. 사실마다 가까운 원본 링크를 둔다. 선택 이유·배움은 공개된 결정 기록이 있을 때만 사실과 나눠 쓴다.
4. 문서 머리의 `sources`와 `relations`에 근거 ID를 연결하고 내부 문서 링크를 건다. 관계는 사람이 읽고 등록한 것으로 표시한다.
5. `python3 scripts/build_wiki.py`로 산출물을 갱신하고 `python3 scripts/build_wiki.py --check`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`를 실행한다. HTML을 PC·모바일에서 읽고 원본 링크와 검색을 확인한다.

빌드가 지원하는 Markdown은 제목, 문단, 순서 있는/없는 목록, 링크, 굵게, 인라인 코드와 코드 블록이다. HTML 원문은 허용하지 않는다. 자동 추출을 하지 않은 지금 관계는 편집 관계이며 Graphify 상태는 `not-run`이다. 공개 원본 변경은 자동으로 해설을 수정하지 않으므로 새 커밋과 설명을 다시 대조한다.
