---
{"id":"standards","type":"criteria","order":50,"mapTitle":"개발 기준 자료","summary":"언어·프레임워크별 선택형 기준과 검증 도구를 제공하는 별도 공개 저장소","sources":["standards-current","standards-python","standards-spring","standards-build","standards-check","standards-ci"],"relations":[]}
---
# Engineering Standards: 선택형 개발 기준과 그 적용 경계

이 저장소는 프로젝트를 시작하거나 변경할 때 사용할 **선택형 기준**을 제공한다. 개인 지식 허브의 전체 목적이 아니라 프로젝트에서 필요할 때 참조할 한 영역이다. README는 공통 원칙·명명·구조 선택, 언어별 프로필, 프레임워크별 프로필을 구분하고, 특정 언어나 아키텍처를 모든 프로젝트에 강제하지 않는다고 밝힌다. 이 문서를 작성했다는 사실만으로 다른 프로젝트에 적용됐다는 뜻도 아니다. [기준 저장소 README](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/README.md)

## 사람이 선택하는 범위

README의 적용 흐름은 기준 저장소 커밋을 고정한 뒤 필요한 문서를 소비 프로젝트에 배치하고, 프로젝트의 기존 지침과 충돌을 검토하는 것이다. 예를 들어 `profiles/languages/python.md`는 이름·모듈·테스트 파일 규칙을 다루되 특정 프레임워크나 런타임 버전을 필수로 하지 않는다. `profiles/frameworks/spring-boot.md`는 새 프로젝트의 네 계층 기본안을 제시하지만 기존 기능별 구조를 먼저 존중한다. 언어 프로필과 프레임워크 프로필은 각각 선택한다. [적용 안내](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/README.md) · [Python 프로필](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/profiles/languages/python.md) · [Spring Boot 프로필](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/profiles/frameworks/spring-boot.md)

## 문서와 공개 위키 생성 경로

`scripts/check_docs.py`는 Markdown 제목, 상대 링크, 코드 블록 닫힘을 검사한다. `scripts/build_wiki.py`는 용어 JSON과 템플릿에서 HTML·Markdown을 생성하고 커밋 SHA를 링크에 넣는다. 이 생성 위키는 기준 저장소의 용어 찾기 도구다. 현재 `kdk-knowledge`의 프로젝트별 Markdown 해설과는 **편집 원본과 설명 대상이 다르다.** [문서 검사 코드](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/scripts/check_docs.py) · [위키 생성 코드](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/scripts/build_wiki.py)

`.github/workflows/docs.yml`은 푸시·PR에 문서·위생·용어·위키·검색 검사를 정의한다. 이는 워크플로 설정의 정적 확인이며, 이 문서에서 해당 커밋의 모든 Actions 결과를 재실행하거나 검증한 것은 아니다. [문서 검사 워크플로](https://github.com/kdkrkwhr/engineering-standards/blob/0ab26dea2102fbb801740ba9f853a004761b7e0c/.github/workflows/docs.yml)

## 이 허브와 연결할 때

[노트버디](notebuddy.md), [옥션스팟 API](auction-spot.md), [AGENT HUB](agent-hub.md)가 어떤 기준을 적용했는지는 프로젝트별 결정 기록과 적용 커밋이 있어야 한다. 지금은 참조 가능한 기준으로만 둔다. 기준 저장소의 Graphify 자동 코드 분석이 있다 해도 이 개인 지식 허브의 Graphify 분석 결과로 대체할 수 없다. 이 허브의 관계는 사람이 등록한 편집 관계이며 자동 추출 상태는 여전히 `not-run`이다.

검토한 기준 커밋은 `0ab26dea2102fbb801740ba9f853a004761b7e0c`다. 개인의 실무 선택 이유나 다른 프로젝트의 실제 적용 결과는 이 저장소 자체에서 증명되지 않는다.
