---
{
  "id": "agent-hub",
  "type": "project",
  "order": 25,
  "summary": "로컬 CLI 에이전트 호출·지속 작업 큐·검토 가능한 작업 사본을 결합한 협업 허브",
  "sources": [
    "agent-hub-readme",
    "agent-hub-entry",
    "agent-hub-server",
    "agent-hub-engine",
    "agent-hub-adapters",
    "agent-hub-discussion",
    "agent-hub-workspace",
    "agent-hub-pipeline",
    "agent-hub-voting",
    "agent-hub-storage",
    "agent-hub-security",
    "agent-hub-project",
    "agent-hub-ci"
  ],
  "relations": [
    {
      "to": "local-queue",
      "label": "에이전트 작업을 SQLite 큐에 기록하고 CLI로 실행",
      "evidence": [
        "agent-hub-engine",
        "agent-hub-adapters",
        "agent-hub-storage"
      ]
    }
  ],
  "mapTitle": "AGENT HUB"
}
---
# AGENT HUB: 로컬 CLI 작업을 연결하는 협업 허브

AGENT HUB RADIO는 설치·로그인된 Claude Code, Codex CLI, Cursor Agent를 로컬 작업 환경에 연결하는 공개 프로젝트다. 자체 모델이나 인증을 제공하는 서버가 아니라 기존 CLI를 호출한다. 터미널에서는 담당자 전환과 다중 에이전트 토론, 웹에서는 채널 대화·독립 투표·역할 분담 작업·상태 화면을 제공한다. README는 `0.3.0 Alpha`, Windows 중심 검증으로 소개한다. **터미널의 로컬 Hub 사용과 웹의 Coral 채널 협업은 필요한 외부 조건이 다르다.** [프로젝트 README](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/README.md) · [CLI 어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

이 글은 README와 주요 코드를 `cfe0ac6b341f6edebbf25655fc2e7867492740bd`에서 정적으로 읽은 결과다. 설치·실행·실제 CLI 통합 테스트를 수행했다는 뜻은 아니다. 저장소의 공개 여부만으로 개인 담당 범위나 단독 기여를 추정하지 않는다.

## 해결하려는 흐름과 모듈 경계

`__main__.py`가 `chat` 명령, 데이터 위치, 인스턴스 잠금과 서버 시작을 다룬다. `server.py`는 정적 웹 화면과 JSON API를 제공하고 요청 출처와 CSRF 토큰을 검사한다. 작업의 지속 상태는 `engine.py`의 SQLite 큐에 저장된다. `adapters.py`는 사용 가능한 CLI를 찾고 공급자별 인자를 구성해 프로세스를 실행·취소하며 응답을 해석한다. [진입점](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/__main__.py) · [HTTP 서버](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/server.py) · [작업 엔진](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/engine.py) · [CLI 어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

`pyproject.toml`은 Python 3.11 이상을 요구하고 Python 런타임 의존성 목록은 비어 있다. HTTP 서버와 SQLite는 표준 라이브러리를 사용한다. 그렇다고 협업 기능에 외부 CLI나 Coral 연결이 필요 없다는 뜻은 아니다. 이 둘은 Python 패키지 의존성과 별개다. [패키지 메타데이터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/pyproject.toml) · [README의 실행 전제](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/README.md)

## 웹 요청에서 에이전트 응답까지

1. 진입점이 데이터 디렉터리와 중복 실행 잠금을 마련한 뒤 Hub와 HTTP 서버를 시작한다. 서버는 루프백 주소 `127.0.0.1`에 바인딩한다. 화면은 `/api/bootstrap`에서 설정·CSRF 토큰, `/api/state`에서 상태를 조회하고 변경은 JSON POST를 사용한다. [진입점](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/__main__.py) · [API 경로](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/server.py)
2. 엔진은 채널 작업을 SQLite에 기록하고 에이전트별 대기 작업을 실행 풀에 넘긴다. 어댑터가 해당 CLI 서브프로세스를 호출한다. 결과는 먼저 DB에 저장한 뒤 채널로 전달하며, 메시지 식별자로 중복 전송 여부를 확인한다. 재시작으로 끊긴 실행은 실패로 기록해 검토 후 재시도할 수 있게 한다. 이는 코드상의 처리 경로이며 실제 장애 복구 성공률을 측정한 결과가 아니다. [엔진](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/engine.py) · [어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

이 지속 작업의 저장·실행 경계는 [로컬 작업 큐](local-queue.md)에 따로 정리했다. 중앙 위키는 실제 코드 경로와 개인적 선택 이유를 구분한다.

## 터미널 토론과 원본 보호

수동 토론은 무제한 상호 호출이 아니다. 호스트가 두 회차를 제어하며, 첫 회차에 참여자가 같은 맥락에서 병렬로 답하고 모두 끝난 뒤 이전 발언을 두 번째 입력에 반영한다. 실행 전후 작업 사본의 지문을 검사하고 일부 실패가 나면 토론을 멈추며 이미 받은 답변은 보존한다. [토론 제어](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/manual_discussion.py)

일반 폴더 작업은 사본과 기준 ZIP, 파일별 SHA-256을 보관한다. 변경 비교로 패치·변경 파일 ZIP·보고서와 추가/수정/삭제 명세를 만들 수 있다. `.git`, 의존성, 캐시, 일부 인증 경로를 기본적으로 제외한다. 이 export는 **원본에 적용하거나 commit·push하는 작업이 아니다.** 파일 크기와 전체 크기·항목 수 제한 및 symlink/junction 거부도 코드에서 확인된다. [작업 사본과 export](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/manual_workspace.py) · [사용 범위](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/README.md)

## 역할, 투표와 실행 증거

파이프라인은 준비·계획·구현·검토를 구분한다. CLI 쓰기 설정은 구현 단계에 적용되고, 검증 명령은 호스트가 실행한다. 명령이 없으면 `skipped` 상태로 남긴다. 검토에는 파일 지문으로 대상 변경을 확인하는 경로가 있다. [단계 구성](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/pipeline.py) · [CLI 실행](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

독립 투표는 공개 전 선택과 근거를 API에서 숨기고 전원 처리 또는 마감 조건에 따라 공개한다. 투표 결과는 판단 자료이지 정답이나 실행 권한 승인이 아니다. [투표 구현](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/voting.py)

## 기술 경계와 확인하지 못한 것

`storage.py`는 설정·DB·로그·작업 사본·산출물 경로를 나누고 이전 저장 구조를 읽는 경로를 유지한다. CLI 인증을 이용하는 구현이므로 모델 서비스로 프롬프트와 작업 내용이 전송될 수 있다. `local-first`를 완전 오프라인이라는 뜻으로 읽으면 안 된다. 보안 문서는 요청 출처·CSRF 보호가 있지만 원격 사용자 인증이 없으므로 공개 프록시 노출을 피하도록 설명한다. 읽기 전용 CLI 설정도 OS 샌드박스와 같지 않다. [저장 경로](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/storage.py) · [보안 설명](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/SECURITY.md) · [CLI 어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

저장소의 Actions 파일에는 세 운영체제와 Python 3.11·3.13의 단위 테스트 및 JavaScript 문법 검사 단계가 정의돼 있다. **설정 존재만 확인했고 CI 성공이나 실제 CLI 통합을 검증하지 않았다.** 선택의 개인적 이유, 사용자 규모, 운영 성과, 단독 기여도 공개 파일만으로 알 수 없다. [테스트 워크플로](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/.github/workflows/tests.yml)
