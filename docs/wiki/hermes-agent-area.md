---
{"id":"hermes-agent-area","type":"project","order":27,"mapTitle":"Hermes Agent Area","summary":"Hermes 프로필·칸반·로그를 2D 사무실 상태로 표현하는 Phaser 화면과 로컬 FastAPI 서버","sources":["area-readme","area-package","area-front","area-connect","area-server","area-test"],"relations":[]}
---
# Hermes Agent Area: 2D 사무실과 로컬 에이전트 상태

공개 README는 Hermes 에이전트들을 픽셀아트 사무실에서 보여 주는 데모와 로컬 실시간 연결을 구분한다. 기술 목록은 Phaser 3·Vite 프런트엔드와 Python FastAPI·WebSocket 백엔드다. 이 문서는 정적 데모와 로컬 서버가 어디에서 갈라지는지 코드로 추적했다. 별도의 설치·실행은 하지 않았다. [프로젝트 README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [프런트 설정](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/package.json)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 공개 화면과 로컬 상태 서버를 분리하고, Pages에서 로컬 WebSocket을 바로 연결할 수 없는 조건을 연결 패널에서 설명한다. [connectPanel.js 39–48·77–96행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)
- **구현 품질 — 보완 필요** 서버의 여러 데이터 위치가 환경변수로 바뀌지만 기본 경로는 한 OS의 폴더 형태에 묶여 있다. 다른 기기에서는 설정 누락 시 빈 데이터나 잘못된 경로를 읽을 수 있다. [server/main.py 21–37행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **운영 준비 — 미확인** 실시간 화면은 별도 로컬 서버와 브라우저 연결에 의존한다. 공개 정적 데모와 로컬 동작을 구분해야 하며 서버 운영 상태는 확인하지 않았다. [connectPanel.js 1–5·77–96행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)
- **유지보수 — 보완 필요** 연결 URL이 기본값·저장값·수동 입력으로 갈라져 환경별 재현 절차를 문서화할 필요가 있다. [connectPanel.js 34–48·70–92행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)

**좋은 점:** 데모와 실제 연결 사이의 제약을 숨기지 않는다. **개선 우선순위:** P2 — 플랫폼별 기본 경로를 제거하고 필요한 경로를 설정·시작 화면에서 명시적으로 검증하면 다른 컴퓨터로 옮길 때의 혼동을 줄인다.

## 화면 진입과 데모 경계

`src/main.js`는 `OfficeScene`을 Phaser 게임으로 시작하고, 연결·알림·카메라·칸반·타임라인 버튼을 붙인다. 서비스 워커 등록 경로도 있다. `connectPanel.js`는 WebSocket과 API 주소를 입력·저장하고 `/api/status`를 조회해 연결 상태를 보여 준다. Pages의 HTTPS에서 로컬 `ws://` 연결이 막히는 경우 안내문을 띄우고 로컬 프런트엔드 또는 별도 `wss://` 연결을 요구한다. 그러므로 공개 Pages 데모를 **실시간 개인 Hermes 데이터가 자동 연결된 화면**이라고 해석하면 안 된다. [프런트 진입](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/main.js) · [연결 패널](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)

## 로컬 서버의 데이터 흐름

`server/main.py`는 프로필 목록을 Hermes CLI에서 읽고, 없으면 파일시스템에서 찾는다. 칸반 DB와 게이트웨이 로그를 읽어 에이전트 상태·활동 타임라인을 만든다. `/api/agents`, `/api/status`, `/api/snapshot`은 상태 조회 경로이고 `/ws`는 스냅샷을 브라우저로 보내는 WebSocket 경로다. 코드상 Hermes 자료는 5초 간격으로 다시 읽고, 장면 상태는 더 짧은 tick 루프에서 보간·전송된다. [서버의 조회·폴링 구현](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

표시 이름은 `area.json`, 로그의 연결 이름, `SOUL.md`, 프로필 폴더명의 순서로 찾는 함수가 있다. 테스트 파일은 게이트웨이 로그의 inbound/response 순서에서 바쁨 상태를 판정하는 사례를 정의한다. **테스트 코드의 존재만 확인했으며 통과를 실행 검증하지 않았다.** [이름·상태 해석](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py) · [정적 확인한 테스트](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/test_gateway_busy.py)

## README 설명과 코드에서 남는 질문

README는 임의 Hermes 경로에서 쓸 수 있다고 소개하지만, 서버 코드에는 환경변수로 바꿀 수 있는 값과 함께 특정 환경을 가정한 기본 경로·cron 식별자도 있다. 이 문서는 하드코딩이 전혀 없다는 문구를 그대로 일반화하지 않는다. 로컬 서버를 실제로 연결했을 때 각 프로필·칸반 데이터가 정확히 표시되는지, 공개 데모에 어떤 mock이 들어 있는지는 이 조사에서 실행 확인하지 않았다. [README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [서버 기본 설정](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

검토 기준은 `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`다. [hermes-env](hermes-env.md)는 Hermes 환경을 배치하는 별도 저장소다. 두 저장소의 자동 설치·직접 의존 관계는 주장하지 않는다. 개인 기여 범위, 매시간 개선이 실제로 실행된 이력이나 성과도 여기서는 검증하지 않았다.
