---
{"id":"hermes-agent-area","type":"project","order":27,"mapTitle":"Hermes Agent Area","summary":"Hermes 프로필·칸반·로그를 2D 사무실 상태로 표현하는 Phaser 화면과 로컬 FastAPI 서버","sources":["area-readme","area-package","area-front","area-connect","area-mock","area-scene","area-server","area-test"],"relations":[{"to":"attendance-pwa","label":"desk-brief가 날씨·뉴스 JSON을 선택적으로 읽고 없으면 cron 결과로 대체","evidence":["area-server"]}]}
---
# Hermes Agent Area: 2D 사무실과 로컬 에이전트 상태

공개 README는 Hermes 에이전트들을 픽셀아트 사무실에서 보여 주는 데모와 로컬 실시간 연결을 구분한다. 기술 목록은 Phaser 3·Vite 프런트엔드와 Python FastAPI·WebSocket 백엔드다. 이 문서는 정적 데모와 로컬 서버가 어디에서 갈라지는지 코드로 추적했다. 별도의 설치·실행은 하지 않았다. [프로젝트 README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [프런트 설정](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/package.json)

**해결 대상은 여러 로컬 에이전트의 활동을 한 장면에서 살펴보는 일**이다. 서버는 프로필·게이트웨이 로그·칸반 상태에서 캐릭터 상태를 만들고, 책상·집중 책상·회의·휴게 공간의 좌표로 움직임을 표현한다. [상태와 좌표를 정의한 서버](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

프런트는 연결·알림·칸반·타임라인 버튼으로 장면을 탐색한다. 공개 화면의 mock과 로컬 서버의 실제 프로필·작업·로그는 출처가 다르므로 캐릭터나 완료 건수를 개인 작업 성과로 읽지 않는다. README의 날씨 파티클·말풍선 등 나머지 기능 목록은 이 글에서 실행 검증하지 않았다. [화면 진입](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/main.js) · [기능 목록](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **보완 필요 · 구조·설계** — 공개 화면과 로컬 서버는 나뉘지만 서버 한 파일이 프로필 탐색, 칸반·로그 해석, 브리프, 파일 미리보기, 상태 방송을 함께 맡는다. 변경 영향 범위가 넓다. 근거: [서버의 기능별 진입점](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **위험 · 구현 품질** — 파일 미리보기의 허용 경로 검사는 정규화된 경로의 문자열 접두사만 비교한다. 이는 실제 경로 포함 관계와 달라 의도한 루트 밖의 텍스트를 읽을 가능성이 있다. 기본 바인딩은 루프백이다. 근거: [파일 미리보기 1456–1488행과 기본 바인딩 1567–1572행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **미확인 · 운영 준비** — 공개 HTTPS 화면에는 로컬 WebSocket 제약 안내가 있고 서버는 기본적으로 루프백에서 시작한다. 실제 연결·데이터 정확도와 다른 환경의 운영 상태는 확인하지 않았다. 근거: [연결 안내](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js) · [서버 시작](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- **보완 필요 · 유지보수** — 두 데이터 루트는 환경변수로 바꿀 수 있지만 기본값은 특정 개인 PC의 경로이고 세 cron 식별자는 상수다. 다른 기기에서 자료가 비면 설정·대체 경로·폴링을 함께 추적해야 한다. 근거: [기본 경로·cron 설정과 브리프 조회](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

**좋은 점:** 데모·로컬 연결의 경계를 UI에 드러내고, 날씨·뉴스 자료에는 대체 경로가 있다. **개선 우선순위:** P1 — 파일 미리보기의 경로 포함 검사를 경로 객체 기준으로 고쳐 조회 범위를 지킨다. P2 — 서버의 조회·브리프·미리보기 책임과 환경별 기본 설정을 분리해 이식성을 높인다.

## 화면 진입과 데모 경계

- `src/main.js`는 `OfficeScene`을 Phaser 게임으로 시작하고 연결·알림·칸반·타임라인 버튼을 붙인다. 서비스 워커도 등록한다. [화면 진입과 버튼](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/main.js)
- 연결 패널은 WebSocket·API 주소를 저장하고 `/api/status`로 상태를 조회한다. HTTPS Pages에서 로컬 `ws://`가 막히는 조건을 설명하고 로컬 프런트엔드나 별도 `wss://` 연결을 안내한다. [연결 패널 39–96행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/connectPanel.js)
- `src/mock.js`에는 **세 프로필**, 가상 칸반 완료 항목, 완료 건수 `[2, 2, 1]`과 평균 속도 고정값이 있다. 이는 mock 생성 경로의 자료이지 개인 Hermes 실적이 아니다. [mock 로스터·칸반·순위값](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/mock.js)
- HTTPS Pages에서 로컬 `ws://`가 차단되면 `OfficeScene`은 연결을 건너뛰고 연결 끊김용 mock 칸반을 갱신한다. 이 분기의 화면 수치까지 항상 앞의 비영 고정값이라고 일반화하지 않는다. [차단 조건](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/mock.js) · [장면의 차단 처리 1163–1169행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/src/scenes/OfficeScene.js)

공개 Pages 화면이 **실시간 개인 Hermes 자료에 자동 연결되는 것은 아니다.** mock 파일의 존재와 실제 브라우저 표시·애니메이션을 실행해 확인한 일도 구분한다.

## 로컬 서버의 데이터 흐름

`server/main.py` 한 파일이 로컬 자료의 조회·해석·전송을 맡는다.

- 폴링은 `hermes profile list` 출력을 파싱하고 결과가 없으면 Hermes 홈의 `config.yaml`·`SOUL.md`를 가진 프로필을 찾는다. [폴링·파일 탐색](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- 칸반 SQLite와 게이트웨이 로그를 읽어 작업 상태와 활동 타임라인을 만든다. [칸반 조회와 폴링](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- HTTP 조회는 `/health`, `/api/agents`, `/api/status`, `/api/snapshot`, `/api/desk-brief`, `/api/file-preview`이고 WebSocket 경로는 장면용 `/ws`와 브리프용 `/ws/desk-brief`다. [라우트 정의 1226–1496행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- 브리프의 날씨·뉴스는 [출퇴근 체크 PWA](attendance-pwa.md) 데이터 폴더의 JSON을 먼저 시도하고 없으면 Hermes cron 출력으로 대체한다. 주식은 cron, 칸반과 파일 트리는 Hermes 자료를 읽는다. PWA 파일은 **선택적 입력**이다. [브리프 조회 1397–1423행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)
- Hermes 자료는 5초마다 다시 읽고 장면 상태는 0.05초 tick에서 보간·방송한다. 이는 코드에 설정된 주기이며 실제 화면 성능 측정은 아니다. [주기와 루프](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

표시 이름은 `area.json` 또는 `office.json`의 설정값 → Discord 연결 이름 → `SOUL.md`에서 읽은 이름 → CLI 프로필 alias → 프로필 ID 순서다. 마지막 ID가 항상 폴더명인 것은 아니다. `default` 프로필의 자료 루트는 Hermes 홈 자체다. [설정·이름 해석 252–340행과 alias 전달 423–449행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

`/api/file-preview`는 텍스트를 제한된 길이로 읽지만, 위 평가에 적은 경로 포함 검사를 고쳐야 조회 범위를 신뢰할 수 있다. [미리보기 1456–1488행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

게이트웨이 로그의 inbound/response 순서로 바쁨 상태를 판정하는 별도 테스트 코드도 읽었다. **테스트 코드는 읽었지만 통과를 실행 검증하지 않았다.** [정적 확인한 테스트](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/test_gateway_busy.py)

## README 설명과 코드에서 남는 질문

README는 임의 Hermes 경로에서 쓸 수 있다고 소개한다. 코드에서는 Hermes 홈과 PWA 데이터 루트를 환경변수로 바꿀 수 있지만 기본값은 특정 개인 PC의 경로이고, 세 cron 식별자는 상수다. 다른 기기에서 빈 자료가 보일 때 먼저 확인할 설정이다. 경로·식별자 값 자체는 이 위키에 다시 싣지 않는다. [README](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/README.md) · [서버 설정 21–35행](https://github.com/kdkrkwhr/hermes-agent-area/blob/e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5/server/main.py)

공개 mock의 구성은 정적으로 확인했다. 로컬 서버를 실제로 연결했을 때 프로필·칸반·브리프가 정확히 표시되는지, 어느 환경에서 운영하는지는 확인하지 않았다.

검토 기준은 `e3e118fa7eb3fcfcd1fd8ca1d88d63763ddb67a5`다. [hermes-env](hermes-env.md)는 Hermes 환경을 배치하는 별도 저장소이고, 이 문서의 관계 지도에는 코드에서 확인한 **선택적 PWA 자료 참조**만 연결했다. 화면 이동 링크와 실제 설치·실행 의존성을 혼동하지 않는다. 개인 기여 범위, 매시간 개선이 실제로 실행된 이력이나 성과도 여기서는 검증하지 않았다.
