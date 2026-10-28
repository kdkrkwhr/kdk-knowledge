---
{"id":"algorithms","type":"project","order":74,"mapTitle":"Java 알고리즘 풀이 기록","summary":"단일 Java 파일에 모은 기초 입력·출력 문제 풀이","sources":["algorithms-1"],"relations":[]}
---
# Java 알고리즘 풀이 기록

**분석 기준:** `e7aacf60b038fff8eb84974d98d138776c46e1c0`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `e7aacf60b038fff8eb84974d98d138776c46e1c0`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 기초 입출력 풀이를 한 파일의 독립 main 클래스로 모은 방식은 개인 학습 기록으로 읽기 쉽다. 재사용 라이브러리 구조를 요구할 목적은 아니다. [TutorialSolution.java 9–73행](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)
- **구현 품질 — 미확인** 이 파일에서 입력·출력 접근은 읽히지만 문제별 입력 조건과 제출 결과가 없어 정답성·경계값 충족을 판단하지 않는다. [TutorialSolution.java의 Main7–Main10, 67–100행](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)
- **운영 준비 — 미확인** 서비스가 아닌 풀이 기록이므로 배포·장애 대응을 평가 기준으로 적용하지 않는다. [TutorialSolution.java 9–28행](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)
- **유지보수 — 보완 필요** Main 번호만으로는 어떤 문제와 제약을 풀었는지 파일 내부에서 찾기 어렵다. 학습 기록의 검색성이 낮아진다. [TutorialSolution.java 9–73행](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)

**좋은 점:** 각 예제가 다른 main 진입점으로 분리돼 있다. **개선 우선순위:** P3 — 문제 식별자·입력 조건을 클래스 옆에 적으면 나중에 풀이를 다시 검토하기 쉬워진다.

## 실제 파일의 형태

공개 소스는 `TutorialSolution.java`의 내부 `Main1`, `Main2` 등 각각 `main` 메서드를 가진 문제 풀이 모음이다. 첫 부분에는 Hello World·날짜 출력·사칙연산·표준 입력 파싱이 있다. 서비스나 재사용 라이브러리라기보다 학습 기록으로 분류한다.
[원본: `src/baekjoon/tuto/TutorialSolution.java`](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)

## 검증 범위

저장소에 독립 빌드·문제 설명·자동 테스트가 없으므로 모든 풀이의 정답 여부와 제출 결과는 판단하지 않았다. 공개 코드에서 확인되는 것은 풀이 접근과 Java 표준 입출력 사용이다.
[원본: `src/baekjoon/tuto/TutorialSolution.java`](https://github.com/kdkrkwhr/algorithms/blob/e7aacf60b038fff8eb84974d98d138776c46e1c0/src/baekjoon/tuto/TutorialSolution.java)

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
