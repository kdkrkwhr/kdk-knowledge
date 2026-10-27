---
{"id":"AgentRadio","type":"reference","order":81,"mapTitle":"AgentRadio fork 참조","summary":"Coral-Protocol upstream 연구 코드의 fork; 독자 커밋 확인 안 됨","sources":["AgentRadio-1","AgentRadio-2","AgentRadio-3"],"relations":[{"to":"agent-hub","label":"다중 에이전트 협업 주제의 별도 upstream fork","evidence":["AgentRadio-1"]}]}
---
# AgentRadio fork 참조

**분석 기준:** `9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 원본 연구와 코드

GitHub fork 메타데이터의 원본은 `Coral-Protocol/AgentRadio`다. README는 여러 코딩 에이전트의 수동적 메시지 수신을 평가하는 연구 코드와 데이터라고 설명한다. `multi_agent/coral_multi_agent.py`는 Harbor 에이전트로 메시지 서버·다중 CLI를 설치하고 실행하는 경로를 정의하며 `resume_guard.py`는 중단된 CLI를 답변 파일이 생길 때까지 재개하는 래퍼를 만든다. 이 코드는 읽기만 했고 실험 결과를 재현하지 않았다.
[원본: `README.md`](https://github.com/kdkrkwhr/AgentRadio/blob/9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645/README.md) [원본: `multi_agent/coral_multi_agent.py`](https://github.com/kdkrkwhr/AgentRadio/blob/9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645/multi_agent/coral_multi_agent.py) [원본: `multi_agent/resume_guard.py`](https://github.com/kdkrkwhr/AgentRadio/blob/9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645/multi_agent/resume_guard.py)

## 기여 구분

2026-10-27 공개 GitHub compare에서는 fork 기본 브랜치가 upstream `main`보다 뒤에 있고 앞선 커밋은 0개였다. fork 자체나 원본 README에 인용된 수치를 계정 소유자의 직접 기여·실험 성과로 귀속하지 않는다. 다른 브랜치·PR 활동은 이 비교만으로 배제할 수 없다.
[원본: `README.md`](https://github.com/kdkrkwhr/AgentRadio/blob/9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645/README.md)

## 사용 경계

재현 스크립트는 컨테이너·외부 모델·서비스 자격 증명 등을 요구할 수 있다. 이 위키 문서 작성을 위해 설치하거나 실행하지 않았다.
[원본: `multi_agent/coral_multi_agent.py`](https://github.com/kdkrkwhr/AgentRadio/blob/9ea8df12f3c3becc5d9b66c4e3b8d796ca5b9645/multi_agent/coral_multi_agent.py)

## 연결해서 읽기

[AGENT HUB](agent-hub.md)는 별도 로컬 협업 프로젝트이며 연구 fork의 수치와 혼동하지 않는다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
