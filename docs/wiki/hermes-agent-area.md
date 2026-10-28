---
{"id":"hermes-agent-area","type":"project","order":27,"mapTitle":"Hermes Agent Area","summary":"Hermes 프로필·칸반·로그를 2D 사무실 상태로 표현하는 Phaser 화면과 로컬 FastAPI 서버","sources":["area-readme","area-package","area-front","area-connect","area-mock","area-server","area-test"],"relations":[{"to":"attendance-pwa","label":"desk-brief가 날씨·뉴스 JSON을 선택적으로 읽고 없으면 cron 결과로 대체","evidence":["area-server"]}]}
---
# Hermes Agent Area: 2D 사무실과 로컬 에이전트 상태

공개 README는 Hermes 에이전트들을 픽셀아트 사무실에서 보여 주는 데모와 로컬 실시간 연결을 구분한다. 기술 목록은 Phaser 3·Vite 프런트엔드와 Python FastAPI·WebSocket 백엔드다. 이 문서는 정적 데모와 로컬 서버가 어디에서 갈라지는지 코드로 추적했다. 별도의 설치·실행은 하지 않았다. [프로젝트 README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [프런트 설정](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/package.json)

프로젝트가 보여 주려는 것은 **여러 로컬 에이전트의 활동을 사무실 책상·상태·칸반·타임라인으로 한눈에 보는 흐름**이다. 공개 Pages에서는 연결 없이 화면과 가상 데이터를 살펴볼 수 있고, 로컬 서버를 연결하면 프로필·작업·로그를 조회한 스냅샷으로 화면을 갱신한다. 두 동선의 데이터 출처를 구분해야 완료 건수나 에이전트 이름을 실제 작업 기록으로 오해하지 않는다. [프런트 진입](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/main.js) · [mock 데이터](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/mock.js) · [서버 폴링](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 보완 필요** 공개 화면과 로컬 서버는 나뉘지만 서버 한 파일이 프로필 탐색, 칸반·로그 해석, 책상 브리프, 파일 미리보기, WebSocket 방송을 함께 맡는다. 기능별 변경 경계가 좁지 않다. [server/main.py의 discover_agent_defs·read_kanban_desk_board·api_desk_brief·api_file_preview·ws_desk_brief, 423–1496행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **구현 품질 — 위험** 파일 미리보기는 경로를 정규화한 뒤 문자열 접두사로만 허용 디렉터리 내부 여부를 판단한다. 문자열 접두사는 실제 경로 포함 관계와 달라 의도한 범위 밖의 텍스트를 읽을 가능성이 있다. 기본 서버 바인딩은 루프백이다. [server/main.py의 api_file_preview, 1456–1488행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py) · [main, 1567–1572행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **운영 준비 — 미확인** 서버는 기본적으로 루프백에서 시작하고 공개 HTTPS 화면의 로컬 WebSocket 제약을 안내한다. 실제 연결·데이터 정확도와 다른 환경에서의 운영 상태는 확인하지 않았다. [server/main.py 1567–1572행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py) · [connectPanel.js 39–48·77–96행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)
- **유지보수 — 보완 필요** 두 데이터 루트는 환경변수로 바꿀 수 있으나 기본값은 특정 PC 형태이고, 세 cron 식별자는 상수다. 다른 환경에서 브리프 데이터가 비면 설정·fallback·폴링을 한 파일에서 함께 추적해야 한다. [server/main.py 21–35·1397–1413·1509–1546행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

**좋은 점:** 데모·로컬 연결의 경계를 UI에 드러내고, 날씨·뉴스 자료에는 대체 경로가 있다. **개선 우선순위:** P1 — 파일 미리보기의 경로 포함 검사를 경로 객체 기준으로 고쳐 조회 범위를 지킨다. P2 — 서버의 조회·브리프·미리보기 책임과 환경별 기본 설정을 분리해 이식성을 높인다.

## 화면 진입과 데모 경계

`src/main.js`는 `OfficeScene`을 Phaser 게임으로 시작하고, 연결·알림·카메라·칸반·타임라인 버튼을 붙인다. 서비스 워커 등록 경로도 있다. `connectPanel.js`는 WebSocket과 API 주소를 입력·저장하고 `/api/status`를 조회해 연결 상태를 보여 준다. Pages의 HTTPS에서 로컬 `ws://` 연결이 막히는 경우 안내문을 띄우고 로컬 프런트엔드 또는 별도 `wss://` 연결을 요구한다. 그러므로 공개 Pages 데모를 **실시간 개인 Hermes 데이터가 자동 연결된 화면**이라고 해석하면 안 된다. [프런트 진입](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/main.js) · [연결 패널](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)

`src/mock.js`에는 연결이 없을 때 쓰는 **세 프로필**과 가상 칸반 완료 항목이 정적으로 들어 있다. 완료 건수 배열도 `[2, 2, 1]`로 정의돼 계급·경험치 표시 계산에 넘겨진다. 이는 코드에 들어 있는 데모 값이라는 사실은 확인했지만, 공개 페이지를 실제로 실행해 표시·애니메이션 결과를 검증한 것은 아니다. 실시간 완료 성과로 읽으면 안 된다. [mock 프로필 9–50행·칸반 147–194행·완료 수 237–256행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/mock.js)

## 로컬 서버의 데이터 흐름

`server/main.py`의 폴링은 Hermes CLI의 프로필 목록을 먼저 읽고, 결과가 없으면 파일시스템에서 찾는다. 칸반 DB와 게이트웨이 로그를 읽어 에이전트 상태·활동 타임라인을 만든다. `/health`는 서버 생존 상태, `/api/agents`·`/api/status`·`/api/snapshot`은 조회 화면의 상태를 제공하고 `/ws`는 스냅샷을 브라우저로 보낸다. 코드상 Hermes 자료는 5초 간격으로 다시 읽고, 장면 상태는 더 짧은 tick 루프에서 보간·전송된다. [서버의 조회·폴링, 1226–1252·1509–1564행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

표시 이름의 순서는 `area.json` → Discord 연결 이름 → `SOUL.md` → Hermes CLI 프로필의 alias → 프로필 ID다. `discover_agent_defs`가 alias를 이름 해석 함수에 전달하므로 원본 README의 간략한 설명보다 이 코드 경로가 정확하다. 별도 테스트 파일은 게이트웨이 로그의 inbound/response 순서에서 바쁨 상태를 판정하는 사례를 정의한다. **테스트 코드는 읽었지만 통과를 실행 검증하지 않았다.** [resolve_display_name·discover_agent_defs, 326–340·423–449행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py) · [정적 확인한 테스트](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/test_gateway_busy.py)

책상 브리프의 `/api/desk-brief`는 날씨·뉴스의 경우 [출퇴근 체크 PWA](attendance-pwa.md) 데이터 폴더의 JSON을 먼저 시도하고, 없으면 Hermes cron 출력으로 대체한다. 주식 항목은 cron 출력, 칸반과 파일 트리는 로컬 Hermes 자료에서 읽는다. 따라서 PWA 자료는 **선택적 입력**이며 서비스가 항상 그 저장소에 의존한다는 뜻은 아니다. `/ws/desk-brief`는 브리프 변경을 전달한다. `/api/file-preview`는 허용 루트 아래 텍스트를 제한된 길이로 읽는 화면 경로지만, 위 평가에 적은 경로 포함 검사를 고쳐야 그 의도한 경계를 신뢰할 수 있다. [api_desk_brief·api_file_preview·ws_desk_brief, 1397–1505행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

## README 설명과 코드에서 남는 질문

README는 임의 Hermes 경로에서 쓸 수 있다고 소개한다. 코드에서는 Hermes 홈과 PWA 데이터 루트 두 곳을 환경변수로 바꿀 수 있지만, 기본값은 특정 컴퓨터의 폴더 형태이고 세 cron 식별자는 상수다. 이 설정 구조는 다른 기기에서 데이터가 비는 이유를 추적할 때 중요하다. 경로와 식별자 값 자체를 이 위키에 다시 싣지 않는다. 로컬 서버를 연결했을 때 프로필·칸반·브리프가 실제로 정확히 표시되는지는 실행 확인하지 않았다. [README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [서버 설정 21–35행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

검토 기준은 `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`다. [hermes-env](hermes-env.md)는 Hermes 환경을 배치하는 별도 저장소이고, 이 문서의 관계 지도에는 코드에서 확인한 **선택적 PWA 자료 참조**만 연결했다. 화면 이동 링크와 실제 설치·실행 의존성을 혼동하지 않는다. 개인 기여 범위, 매시간 개선이 실제로 실행된 이력이나 성과도 여기서는 검증하지 않았다.
