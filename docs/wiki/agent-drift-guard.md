---
{"id":"agent-drift-guard","type":"project","order":29,"mapTitle":"Agent Drift Guard","summary":"에이전트 메시지를 단계 경계까지 버퍼링하는 실험 코드; README는 Hermes 대상 중단을 명시","sources":["drift-readme","drift-buffer","drift-inject","drift-test","drift-hook","drift-session"],"relations":[]}
---
# agent-drift-guard: 단계 경계에 메시지를 전달하는 연구 코드

README는 이 저장소의 상태를 **SHELVED**라고 명시한다. Hermes에는 `AIAgent.steer()`와 busy 입력 경로가 이미 있어, Hermes 대상의 별도 0-turn 메커니즘 개발을 중단했다고 설명한다. 따라서 이 문서는 현재 운영 중인 Hermes 필수 구성요소를 소개하는 글이 아니라, 공개된 실험 코드와 중단 판단을 정리한다. [상태와 배경](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/README.md)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `7b655505e4c893590b02f7f391e3bba7f73275be`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 메시지 수신과 단계 종료 시 방출을 작은 버퍼 계약으로 분리했다. [buffer.py의 DriftGuardBuffer, 10–40행](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/src/drift_guard/buffer.py)
- **구현 품질 — 보완 필요** 수신 메시지는 제한 없이 목록에 쌓인다. 단계 종료가 오래 오지 않는 실행 환경에서는 메모리 사용과 한 번에 주입할 문맥 크기가 늘 수 있다. [buffer.py 17–36행](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/src/drift_guard/buffer.py)
- **운영 준비 — 미확인** README가 Hermes 핵심 기능으로 대체되어 보류 상태라고 명시한다. 현재 서비스 운영 준비도를 억지로 판정할 대상이 아니다. [README.md 1–10행](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/README.md)
- **유지보수 — 양호** 보류 이유와 재개 조건을 문서에 남겨 중복 구현을 피할 수 있다. [README.md 3–10행](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/README.md)

**좋은 점:** 동시 수신과 방출을 잠금 안의 목록 교체로 처리한다. **개선 우선순위:** P2 — 다른 런타임을 대상으로 재개할 때 큐 상한·중복 처리·과부하 정책을 먼저 정한다. 보류 중인 Hermes용 구현에 즉시 운영 감점을 주지는 않는다.

## 어떤 문제를 코드로 다루나

다른 에이전트의 메시지가 추론이나 도구 호출 중간에 도착하면 현재 흐름을 흐트러뜨릴 수 있다는 가설에서 출발한다. `DriftGuardBuffer.on_message`는 메시지를 잠금 아래 대기 목록에 넣고 모델을 호출하지 않는다. `on_step_end`는 현재 목록을 교체해 돌려주므로 경계 뒤에 도착한 메시지가 다음 회차로 남는다. `pending_count`는 남은 수를 읽는다. [버퍼 구현](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/src/drift_guard/buffer.py)

`format_injection`은 메시지 타입을 검사하고 발신자·본문을 텍스트 블록으로 만든다. 기본 위치는 도구 결과의 뒤다. `inject_at_boundary`는 Hermes 어댑터의 대기 블록을 꺼내 도구 결과에 덧붙인다. **메시지를 같은 턴에 실제로 넣고 새 LLM 턴을 열지 않는 것은 연결한 런타임의 책임**이다. 핵심 함수만으로 모든 에이전트 런타임의 0-turn 동작을 보장하지 않는다. [포맷터](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/src/drift_guard/inject.py) · [Hermes 훅](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/hermes_plugin/agent-drift-guard/inject_hook.py)

## 세션과 검증 코드

Hermes 플러그인 쪽 `SessionGuards`는 세션 ID별 버퍼와 라디오 watcher를 관리하고 종료 시 제거한다. watcher는 선택적이고, 없으면 수동으로 넣은 메시지만 다룬다. `tests/test_buffer.py`는 메시지를 넣어도 즉시 비워지지 않는 경우, 단계 종료 후 두 메시지 flush, 빈 flush를 정의한다. **테스트 파일을 읽었지만 실행하지 않았다.** [세션 관리](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/hermes_plugin/agent-drift-guard/session_guards.py) · [버퍼 테스트](https://github.com/kdkrkwhr/agent-drift-guard/blob/7b655505e4c893590b02f7f391e3bba7f73275be/tests/test_buffer.py)

## 이 기록의 상태

검토 기준은 `7b655505e4c893590b02f7f391e3bba7f73275be`다. README가 언급한 Hermes 본체 구현을 이 문서에서 독립적으로 재검증하지 않았고, 벤치마크나 다른 런타임 어댑터 성과도 확인하지 않았다. [AGENT HUB](agent-hub.md)와 같은 멀티 에이전트 영역의 문제를 다루지만 실제 통합 관계를 주장하지 않는다. 개인의 기여 범위·선택 이유는 별도 근거가 필요하다.
