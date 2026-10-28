---
{
  "id": "notebuddy",
  "type": "project",
  "order": 10,
  "summary": "그림·사진에서 시작한 친구의 행동을 공통 Python 규칙으로 계산하는 공개 프로젝트",
  "sources": [
    "notebuddy-readme",
    "notebuddy-api",
    "notebuddy-ports",
    "notebuddy-web",
    "notebuddy-anna",
    "notebuddy-anna-plugin",
    "notebuddy-store",
    "notebuddy-evolution"
  ],
  "relations": [
    {
      "to": "python-execution",
      "label": "웹과 Anna가 Python 전이 함수를 호출",
      "evidence": [
        "notebuddy-api",
        "notebuddy-web",
        "notebuddy-anna"
      ]
    }
  ],
  "mapTitle": "노트버디"
}
---
# 노트버디: 한 친구의 규칙을 여러 화면에서 실행하기

노트버디는 그림이나 사진에서 친구를 만들고, 돌봄·대화·산책·모험을 이어 가는 공개 프로젝트다. 이 문서는 사용 안내를 다시 나열하기보다 **화면에서 선택한 행동이 어떤 코드에서 판정되고 저장되는지**를 따라간다. 제품 범위는 [프로젝트 README](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/README.md)를 기준으로 읽었다. 이 문서가 기술 선택의 개인적 동기나 담당 범위를 증명하지는 않는다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `ca5648b49e6d0a67526856a930090173d0454389`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 상태 전이와 저장 결정을 분리하고 실행 입력을 주입한다. [game_api.py의 transition·GameApplication, 50–111행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py)
- **구현 품질 — 양호** 공통 GameApplication은 요청 ID와 저장 리비전을 검사하고 충돌 시 재시도하며, Anna의 별도 GameService는 기존 APS 행에 ETag 조건부 쓰기를 쓴다. 두 저장 경로를 동일한 보장으로 취급하지 않는다. [game_api.py 81–111행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py) · [notebuddy_plugin.py 128–183행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/notebuddy_plugin.py)
- **운영 준비 — 보완 필요** Anna APS 경로의 최초 생성에는 원자적 create-if-absent가 없고 쓰기 직전 재조회로 경쟁 가능성만 줄인다. 기존 행의 ETag 보호와 다른 경계다. 실제 동시 사용 충돌 빈도·운영 규모는 확인하지 않았다. [notebuddy_plugin.py 164–178행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/notebuddy_plugin.py)
- **유지보수 — 보완 필요** Dependency가 실행 문맥이 없을 때 다른 모듈로 암묵적으로 넘어간다. 직접 헬퍼 호출과 정상 전이에서 입력 출처가 달라져 추적이 어려울 수 있다. [ports.py의 ContextMapping·Dependency, 71–113행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/ports.py)

**좋은 점:** 공통 규칙 계산과 호스트별 저장 책임을 분리하고 Anna의 기존 저장에는 ETag·요청 영수증을 사용한다. **개선 우선순위:** P1 — APS 최초 생성에도 원자적 생성 조건을 제공할 수 있는지 확인해 첫 저장 경쟁의 경계를 닫는다. P2 — 암묵적 실행 문맥 대체 경로를 명시적 어댑터로 분리한다.

## 해결 대상과 사용자 흐름

공개 README의 사용자 흐름은 그림·사진 또는 랜덤 선택으로 친구를 만나는 데서 시작한다. 이후 먹이, 놀이, 훈련, 수면, 대화로 상태와 경험을 쌓고 산책·던전을 탐색한다. 진화는 레벨만 올랐다고 즉시 일어나지 않는다. 활동 조건을 채운 뒤 사용자가 시점을 정하고 세 방향 중 하나를 고른다. AI는 방향 설명과 외형 제안을 보탤 수 있지만, 어떤 방향을 선택할지는 사용자에게 남는다. [기능 설명 원본](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/README.md)

이 흐름에는 게임 규칙, 플랫폼별 화면과 저장, AI가 만드는 표현이 섞여 있다. 공개 코드에서 확인되는 경계를 분리해 읽어야 한다. 세부 실행 환경은 [Python 실행 경계](python-execution.md)에 모았다.

## 실제 구조: 상태 전이와 실행 환경

공통 진입점인 `engine/game_api.py`의 `transition`은 기존 상태, 명령, 실행 문맥을 받아 결과와 다음 상태, 변경 여부, 이벤트를 담은 `TransitionResult`를 돌려준다. 이 함수 안에서 명령 형식과 접근 범위를 검사한 뒤 엔진 명령을 분배한다. 파일 저장은 이 함수가 직접 수행하지 않는다. 별도의 `GameApplication`은 저장소에서 상태를 읽고, 전이 결과가 바뀌었을 때 리비전을 확인하며 교체한다. [전이 함수와 저장 경계](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py)

`ExecutionContext`에는 규칙 데이터, 템플릿, 현재 시각, 난수원, ID 생성기가 들어간다. 즉 전이 계산에 필요한 외부 입력을 호출자가 건네는 형태다. 저장소 계약은 `load`와 `compare_and_set`으로 드러난다. 이것은 코드에서 관찰한 의존 경계이며, 그렇게 설계한 개인적 이유는 공개 근거만으로 확정할 수 없다. [실행 문맥과 저장소 계약](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/ports.py)

## 주요 실행·데이터 흐름

1. 웹 Worker는 Pyodide를 준비하고 Python 코어 파일과 규칙 데이터를 브라우저 환경에 적재한다. 메시지를 받으면 `transition`을 호출하고 결과·상태·화면용 뷰를 다시 JavaScript 쪽으로 보낸다. [웹 Worker 원본](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/worker.js)
2. Anna Worker는 허용 명령을 확인하고 게임 코어의 `transition`을 호출한다. 반환값에는 결과, 상태, 변경 여부와 뷰가 들어간다. 상위 `GameService.invoke`는 APS에 저장된 값·ETag를 읽고 요청 영수증과 게임 상태를 함께 구성해 조건부로 쓴다. 기존 행은 ETag 충돌을 재시도하지만 최초 생성은 쓰기 전 재조회만 하며 원자적 생성 조건을 보장하지 않는다. `GameApplication`의 일반 저장소 계약을 Anna 구현에 그대로 적용했다고 읽으면 안 된다. [Anna Worker](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/game_worker.py) · [Anna 저장 오케스트레이션 128–183행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/notebuddy_plugin.py) · [공통 계약 81–111행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py)
3. 웹 저장 모듈은 IndexedDB의 `saves` 저장소에서 플레이어 상태를 읽고 리비전을 비교해 갱신한다. 플레이어와 그림 데이터를 별도 키로 관리하며, 교체할 때는 같은 트랜잭션을 사용한다. 이 사실은 웹 구현에 한정된다. [웹 저장 코드](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/store.js)

진화 코드에서는 다음 단계의 레벨·돌봄·훈련·산책 등 조건을 계산하고, 진행 중인 선택을 먼저 끝내야 하는 상황을 구분한다. 후보 방향을 예약·선택하는 흐름이 있으며, AI 설명은 게임 조건 자체를 결정하는 값과 분리돼 있다. 여기서는 코드의 경계를 설명할 뿐 실제 배포판의 모든 화면 상태를 재검증했다고 주장하지 않는다. [진화 규칙 원본](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/evolution.py)

## 확인한 기술과 연결 문서

- **Python**: 공통 상태 전이 함수와 게임 규칙 코드. [game_api.py](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py)
- **Pyodide·JavaScript Worker**: 브라우저에서 Python 전이를 호출하는 경로. [web/worker.js](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/worker.js)
- **IndexedDB**: 공개 웹 저장 모듈의 상태 저장소. [web/store.js](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/store.js)
- **APS ETag·요청 영수증**: Anna의 기존 저장 충돌 검사와 반복 요청 처리에 쓰는 별도 경로. 최초 생성은 같은 원자성을 확인하지 못했다. [notebuddy_plugin.py 128–183행](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/notebuddy_plugin.py)

기술의 역할과 근거 파일은 [Python 실행 경계](python-execution.md)에서 다시 연결한다. 다른 사례가 README와 코드에서 어떻게 출발하는지는 [옥션스팟 API](auction-spot.md)를 보자.

## 확인 범위와 남은 질문

이 문서는 `ca5648b49e6d0a67526856a930090173d0454389` 커밋의 공개 README와 위 파일만 대조했다. 어느 기능을 김동기가 직접 맡았는지, 왜 Python·Pyodide 경계를 선택했는지, 운영 성과가 무엇인지는 이 근거로 알 수 없다. 이후 공개 가능한 결정 기록이나 회고가 생기면 사용 사실과 선택 이유를 분리해 추가한다. 원본 저장소의 별도 위키는 이 중앙 문서를 작성하기 위한 필수 입력이 아니다.
