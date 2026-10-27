---
{
  "id": "local-queue",
  "type": "implementation",
  "order": 45,
  "summary": "AGENT HUB의 SQLite 작업 상태와 CLI 서브프로세스 사이의 처리 경계",
  "sources": [
    "agent-hub-engine",
    "agent-hub-adapters",
    "agent-hub-storage",
    "agent-hub-security"
  ],
  "relations": [],
  "mapTitle": "로컬 작업 큐"
}
---
# 로컬 작업 큐: 기록한 상태와 CLI 실행의 경계

[AGENT HUB](agent-hub.md)는 웹 요청을 곧바로 모델 응답으로 취급하지 않는다. `engine.py`가 에이전트별 작업을 SQLite에 기록하고 실행 상태를 관리하며, `adapters.py`가 실제 설치된 CLI를 서브프로세스로 호출한다. 결과는 데이터베이스에 남긴 다음 채널 전달을 시도한다. 이 순서는 공개 코드에서 관찰한 처리 흐름이다. [작업 엔진](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/engine.py) · [CLI 어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py)

## 재시작과 전달 상태

엔진은 끊긴 실행을 실패 상태로 표시하고, 채널 메시지의 작업 식별자를 확인해 이미 전달된 응답을 중복 전송하지 않도록 한다. 이는 **재검토 가능한 상태를 남기는 코드 경로**이지 실서비스에서 모든 오류가 회복된다는 보장이 아니다. 설정, DB, 로그, 작업 사본, 산출물 경로는 저장 모듈에서 분리된다. [엔진 상태 처리](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/engine.py) · [저장 경로](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/storage.py)

## 로컬의 의미

큐와 웹 서버가 로컬에 있어도 CLI는 로그인된 외부 모델 서비스에 작업을 보낼 수 있다. 따라서 이 구현을 오프라인 전용이라고 부르지 않는다. 공개 보안 문서는 원격 사용자 인증이 없는 로컬 UI의 공개 노출을 피하도록 설명한다. [어댑터](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/adapters.py) · [보안 설명](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/SECURITY.md)

이 큐의 선택 이유·처리량·운영 효과는 확인한 파일에 없다. 프로젝트에서 관찰한 기술 사용 사실과 경험에서 도출한 개인 기준은 추후 별도 근거가 있어야 연결된다.
