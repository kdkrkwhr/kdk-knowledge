---
{
  "id": "python-execution",
  "type": "technology",
  "order": 30,
  "summary": "노트버디의 공통 Python 전이 함수와 브라우저·Anna 호출 경계",
  "sources": [
    "notebuddy-api",
    "notebuddy-ports",
    "notebuddy-web",
    "notebuddy-anna",
    "notebuddy-store"
  ],
  "relations": [],
  "mapTitle": "Python 실행 경계"
}
---
# Python 실행 경계: 공통 규칙과 서로 다른 호출자

[노트버디 사례](notebuddy.md)에서 확인한 Python의 역할은 화면 기술 전체가 아니라 **게임 상태 전이 계산**이다. `engine/game_api.py`의 `transition`은 상태·명령·`ExecutionContext`를 받아 결과와 다음 상태를 돌려준다. 실행 문맥에는 시각·난수원·ID 생성기 등 계산에 필요한 외부 입력이 담긴다. [전이 코드](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/game_api.py) · [실행 포트](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/engine/ports.py)

## 두 호출 경로

브라우저의 JavaScript Worker는 Pyodide로 Python 코어를 적재하고 메시지를 `transition`에 전달한다. Anna Worker도 허용 명령을 확인한 뒤 같은 전이 함수로 들어간다. 두 Worker의 입력·출력 처리가 같다는 주장이 아니라, **게임 규칙의 진입점이 같다**는 관찰이다. [브라우저 Worker](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/worker.js) · [Anna Worker](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/anna/executas/notebuddy/game_worker.py)

웹의 저장은 전이 계산과 별도로 `web/store.js`가 IndexedDB에 수행한다. 코드에는 리비전을 비교한 갱신 경로가 있다. 이 저장 방식을 Anna의 영속화 방식으로 일반화하지 않는다. [브라우저 저장](https://github.com/kdkrkwhr/notebook-pets/blob/ca5648b49e6d0a67526856a930090173d0454389/web/store.js)

## 사실과 아직 없는 해석

공개 파일은 함수의 역할과 호출 경로를 보여 준다. Python을 선택한 개인적 이유, 대안 비교, 이 구조의 성능·운영 결과는 이 파일들만으로 확인할 수 없다. 향후 결정 기록이 공개되면 사용 사실과 이유를 따로 적는다.
