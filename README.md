# kdk-knowledge

김동기의 프로젝트, 경력과 역할, 기술 선택과 배움, 경험에서 나온 개발 기준을 **공개 근거와 연결**하기 위한 개인 지식 허브입니다. 개발 기준은 한 영역입니다. 아직 근거가 등록되지 않은 경력·성과·기술 선택은 공개 위키에 빈 상태로 남깁니다.

- [프로젝트 중심 위키](https://kdkrkwhr.github.io/kdk-knowledge/)
- [실제 Markdown 위키 문서](https://kdkrkwhr.github.io/kdk-knowledge/wiki/)
- [근거 관계 지도](https://kdkrkwhr.github.io/kdk-knowledge/architecture/)
- [입력 템플릿](templates/README.md)

## 현재 범위

첫 대표 사례는 공개 [Notebook Pets](docs/wiki/notebuddy.md), [Auction Spot API](docs/wiki/auction-spot.md), [AGENT HUB](docs/wiki/agent-hub.md)입니다. [공개 저장소 28개의 문서 목록](docs/wiki/repositories.md)에 각 저장소의 정적 검토 범위와 fork 구분을 기록했습니다. 다른 저장소에 위키가 있어야 연결되는 구조가 아닙니다. 원본 저장소는 수정하거나 자동 동기화하지 않습니다. [Engineering Standards](docs/wiki/standards.md)는 참고할 개발 기준으로 별도 기록했으며, 사례 프로젝트에 실제 적용됐다고 표시하지 않습니다.

현재 확인한 공개 저장소 28개 모두 문서를 작성했습니다. 작은 저장소는 단일 파일, 큰 저장소는 대표 구현 파일로 범위를 제한했습니다. 전체 과거 프로젝트·경력 자료의 수집이나 원본 프로젝트의 실행 검증을 마친 상태는 아닙니다. 개인 역할·성과·선택 이유는 별도 근거가 생길 때 보강합니다.

`docs/wiki/*.md`가 해설의 편집 원본입니다. 문서 머리의 메타데이터가 출처·관계를 등록하고, `docs/wiki/sources.json`에 고정 커밋의 공개 URL을 보관합니다. `scripts/build_wiki.py`가 HTML, 원본 Markdown 사본, 본문 검색 색인과 `site/knowledge.json`을 함께 생성합니다. `site/index.html`은 프로젝트 진입 화면이고, `site/architecture/`는 문서에서 파생한 편집 관계를 탐색합니다. Graphify는 `docs/wiki/*.md`만 입력으로 실행하며 결과를 `docs/graph/graph.json`에 커밋합니다(`scripts/sync_graph.py`). 빌드는 이 파일에서 개념 항목·자동 추출 관계·`site/wiki/topics.html`(주제 지도)을 만들고, 편집 관계와 `origin`으로 구분합니다. Graphify의 대화형 뷰어는 `site/graph/`에 그대로 싣습니다(vis-network CDN 사용).

## 추가와 검증

1. [문서 갱신 절차](docs/wiki/maintenance.md)에 따라 원본 README·코드·문서를 고르고 공개 여부를 확인합니다. 위키 유무는 수집 조건이 아닙니다. 경력·역할·배움은 [입력 템플릿](templates/README.md)을 사용합니다. 비공개 초안은 이 공개 저장소에 저장하지 않습니다.
2. `docs/wiki/sources.json`에 전체 커밋 SHA의 공개 파일 URL을 등록하고, `docs/wiki/*.md`에 출처·관계·본문을 작성합니다. 지원 구문은 제목, 문단, 목록, 링크, 굵게, 인라인 코드, 코드 블록입니다. 원본 HTML은 허용하지 않습니다.
3. 문장과 원본을 사람이 다시 대조한 뒤 `python3 scripts/build_wiki.py`를 실행합니다. README 문장과 실제 코드·설정·의존성·테스트가 다르면 차이를 기록합니다. 정적 소스 확인과 실행 검증도 구분합니다. 근거 변경만으로 해설이 자동 수정되지는 않습니다.
4. `python3 scripts/build_wiki.py --check`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`를 실행합니다. 정적 파일은 `python3 -m http.server 8000 -d site`로 미리 볼 수 있습니다.
5. GitHub Actions가 공개 산출물 `site/`만 검사 후 Pages에 업로드합니다. 실제 공개 여부는 Actions와 URL 응답을 별도로 확인합니다.

외부 LLM 호출, 유료 API, 실시간 챗봇은 현재 흐름에 없습니다. Graphify 추출은 작성자 PC에서 Claude Code 세션으로 실행하고 산출물만 커밋합니다.
