---
{"id":"hermes-team-hub","type":"project","order":28,"mapTitle":"Hermes Team Hub","summary":"역할별 팀 로그의 정적 데모와 Hermes 상태를 읽는 로컬 서버를 분리한 허브","sources":["team-readme","team-web","team-store","team-server","team-cli","team-model"],"relations":[]}
---
# hermes-team-hub: 정적 팀 로그와 로컬 실시간 화면

이 저장소는 PM·Dev·Infra·QA·Ops 역할별 입력 화면과 팀 로그를 보여 준다. 공개 README는 Pages를 **정적 데모**, `local/app.py`를 Hermes 칸반·프로필·Coral 상태를 읽는 **로컬 실행형**으로 구분한다. 같은 이름의 허브라도 데이터 출처가 다르므로 두 경로를 합쳐 실시간 서비스로 설명하지 않는다. [README](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/README.md)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `1406ee05e3ea21a9e0c53aa0856879c976cd3ac5`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** Pages의 브라우저 저장 기록과 로컬 서버의 Hermes 조회를 별도 경로로 둔다. [js/store.js 1–18행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/store.js) [local/app.py 1–17행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py)
- **구현 품질 — 위험** 로컬 HTTP의 GET 경로가 허용 목록의 일부 상태 변경 Hermes 명령을 실행하고, 응답은 모든 Origin을 허용하며 요청 출처 검사가 보이지 않는다. 루프백 서비스라도 다른 웹 페이지에서 요청을 유도할 가능성을 고려해야 한다. 실제 외부 호출은 확인하지 않았다. [local/app.py의 Handler, 1091–1136·1221–1224행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py)
- **운영 준비 — 보완 필요** 서버는 루프백에 바인딩하지만 프로필 기본 위치는 특정 PC 형태다. 다른 기기에서 데이터 위치를 설정해야 하고, 로컬 명령 API의 브라우저 접근 경계도 보완해야 한다. [local/app.py 29–31·1091–1097·1263–1268행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py)
- **유지보수 — 보완 필요** 정적 기록은 한 브라우저의 localStorage에만 저장된다. 팀 공유 기록으로 해석하지 않도록 데이터 범위와 백업 방법을 유지해야 한다. [js/store.js 6–31행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/store.js)

**좋은 점:** 정적 기록과 로컬 실시간 조회의 데이터 경계를 나눴고 CLI 명령은 허용 목록으로 제한한다. **개선 우선순위:** P1 — 상태 변경 명령을 읽기 GET에서 분리하고 요청 출처·확인 경계를 두어 로컬 API의 의도하지 않은 호출을 줄인다. P2 — 역할별 칸반 필터 상태와 프로필 기본 위치를 정리한다. [명령 허용 목록 1100–1136행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py) · [공유 필터 128–185행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/app.js)

## Pages 쪽의 기록 흐름

`js/app.js`는 역할 탭과 대시보드를 렌더링한다. `js/store.js`의 `HubStore`는 `hermes-team-hub.logs.v1` 키로 입력한 기록을 브라우저 `localStorage`에 추가·조회·삭제하고 날짜·역할로 정렬한다. 이 데이터는 브라우저별 로컬 상태다. 다른 팀원의 기기와 자동 공유되는 DB가 아니다. [화면 로직](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/app.js) · [브라우저 저장소](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/store.js)

## 로컬 실행형의 데이터 흐름

`local/app.py`는 Python 표준 라이브러리 `ThreadingHTTPServer`를 루프백 주소에 바인딩한다. `/api/kanban`은 `hermes kanban list --json`을 호출해 결과를 변환하고 5초 메모리 캐시를 둔다. `/api/agents`는 프로필의 SOUL 문서에서 표시 정보를 읽고, `/api/coral`, `/api/logs` 등의 로컬 조회 경로가 있다. 일부 POST API는 로컬 JSON을 저장한다. 별도의 GET 경로는 허용 목록의 Hermes 명령을 실행하며 이 목록에는 상태 변경 명령도 있다. 이는 읽기 전용 상태 조회와 구분해야 한다. 개인 PC 자료를 다루므로 Pages 데모의 공개 데이터와 혼동해서는 안 된다. [로컬 HTTP 서버의 GET·POST, 1162–1257행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py) · [명령 허용 목록 1100–1136행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/app.py)

`local/team_hub.py`는 `log`, `view`, `timeline`, `report`, `reset` 명령을 분기한다. 공통 모델의 `append_activity`는 역할을 검사하고 시각을 채워 `activities.jsonl`에 기록하며 `load_activities`는 날짜·역할·카드·태그 필터로 읽는다. JSONL 모델과 정적 Pages의 localStorage는 별도 저장 방식이다. [CLI](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/team_hub.py) · [JSONL 모델](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/local/team_hub/model.py)

정적 화면의 칸반 검색·상태 필터는 하나의 전역 상태를 공유한다. 역할별 검색 입력은 따로 저장하지만 탭 전환 후 필터가 섞일 수 있다. 이 판단은 코드의 상태 공유에서 나온 것이며 실제 화면 증상을 실행해 확인한 것은 아니다. [js/app.js 128–185행](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/js/app.js)

## 아직 확인하지 않은 연결

README는 [hermes-env](hermes-env.md)의 SOUL 파일로 소개 카드를 생성하는 연계를 예정이라고 표현한다. 이것은 완료된 자동 동기화의 근거가 아니다. 로컬 서버를 실행해 실제 Hermes·Coral 연결을 확인하지 않았고, 다른 기기 사이의 동기화도 검증하지 않았다. [연계 상태 원문](https://github.com/kdkrkwhr/hermes-team-hub/blob/1406ee05e3ea21a9e0c53aa0856879c976cd3ac5/README.md)

기준 커밋은 `1406ee05e3ea21a9e0c53aa0856879c976cd3ac5`다. 역할·데이터 분리는 코드로 확인했지만, 김동기의 개인 담당 범위와 설계 선택 이유·운영 성과는 확인하지 못했다.
