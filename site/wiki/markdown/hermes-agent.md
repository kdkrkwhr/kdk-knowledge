---
{"id":"hermes-agent","type":"reference","order":80,"mapTitle":"Hermes Agent fork 변경 범위","summary":"NousResearch upstream의 fork와 기본 브랜치에 확인된 두 변경 커밋","sources":["hermes-agent-1","hermes-agent-2","hermes-agent-3","hermes-agent-4","hermes-agent-5"],"relations":[]}
---
# Hermes Agent fork 변경 범위

**분석 기준:** `b1e211ddd15cc72e99aa068254b89e4351f8c278`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `b1e211ddd15cc72e99aa068254b89e4351f8c278`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 확인된 fork 변경은 upstream 전체 기능이 아니라 릴리스 태그 수집과 격리 환경의 CA 설정에 한정된다. 변경 목적과 대상 파일이 분명하다. [install-e2e.yml 75–91행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/.github/workflows/install-e2e.yml) [stage2-run.sh 216–223행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/sandbox/stage2-run.sh)
- **구현 품질 — 미확인** 격리 환경에만 CA 경로를 주는 구성은 보이지만 실제 네트워크 격리와 설치 결과는 정적 파일만으로 확인할 수 없다. upstream 전체 구현을 계정의 작업으로 평가하지 않는다. [dev-sandbox.sh 75–87행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/dev-sandbox.sh) [stage2-run.sh 216–230행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/sandbox/stage2-run.sh)
- **운영 준비 — 미확인** 설치 E2E 워크플로는 개발 검증 경로이지 개인 서비스 운영 경로가 아니다. [install-e2e.yml 3–23행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/.github/workflows/install-e2e.yml)
- **유지보수 — 보완 필요** upstream 태그를 조건부로 가져오므로 fork에서 어떤 upstream 기준과 변경분을 유지할지 기록하지 않으면 이후 동기화 판단이 어려워진다. [install-e2e.yml 75–91행](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/.github/workflows/install-e2e.yml)

**좋은 점:** fork 전용 변경의 범위가 비교적 작고 CA 신뢰 경로를 격리 환경에 둔다. **개선 우선순위:** P3 — upstream 기준 커밋과 두 fork 변경의 목적을 갱신 기록에 남긴다. 이 평가는 upstream 제품 품질이나 개인 기여 전반의 판정이 아니다.

## upstream과 fork

GitHub 메타데이터의 원본은 `NousResearch/hermes-agent`다. README는 Nous Research가 만든 에이전트의 모델·채널·도구·학습 경로를 설명하고, `package.json`은 데스크톱·웹·TUI 작업공간을 열거한다. 이 광범위한 upstream 기능을 이 계정의 단독 개발이라고 쓰지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/README.md) [원본: `package.json`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/package.json)

## fork 고유 변경의 정적 범위

2026-10-27 공개 compare에서 fork 기본 브랜치는 upstream `main` 대비 앞선 커밋 두 개였다: `d88c1cb0852ca7f8525d77cb0730fe7f4c6b786b`는 미태그 fork에서 upstream release tag를 얻는 CI 변경, `b1e211ddd15cc72e99aa068254b89e4351f8c278`는 sandbox 안의 npm TLS 프록시 CA 신뢰 변경이다. 변경 파일은 설치 E2E 워크플로와 두 sandbox 스크립트다. fork의 다른 브랜치나 실제 사용자·PR 작성자까지 확정하는 주장은 아니다.
[원본: `.github/workflows/install-e2e.yml`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/.github/workflows/install-e2e.yml) [원본: `scripts/dev-sandbox.sh`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/dev-sandbox.sh) [원본: `scripts/sandbox/stage2-run.sh`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/sandbox/stage2-run.sh)

## 실행 경계

스크립트는 설치 환경을 변경할 수 있는 실행 코드지만 여기서는 읽기만 했다. CA·패키지 설치 경로의 실제 동작·보안 적합성은 검증하지 않았다. fork 자체를 실행하거나 원본을 수정하지 않았다.
[원본: `scripts/dev-sandbox.sh`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/dev-sandbox.sh) [원본: `scripts/sandbox/stage2-run.sh`](https://github.com/kdkrkwhr/hermes-agent/blob/b1e211ddd15cc72e99aa068254b89e4351f8c278/scripts/sandbox/stage2-run.sh)

## 연결해서 읽기

[Hermes 환경](hermes-env.md), [Agent Area](hermes-agent-area.md), [Team Hub](hermes-team-hub.md)는 계정의 별도 저장소이며 이 fork의 upstream 제품과 혼동하지 않는다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
