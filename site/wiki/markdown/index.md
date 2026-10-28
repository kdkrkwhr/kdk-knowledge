---
{"id":"index","type":"guide","order":0,"summary":"공개 프로젝트의 구현을 읽고 근거 문서와 관계를 따라가는 중앙 위키","sources":[],"relations":[]}
---
# 프로젝트에서 시작하는 위키

이곳은 김동기의 공개 GitHub 저장소에서 확인한 내용을 **이 저장소의 Markdown 문서**로 정리한 중앙 위키다. 원본 저장소에 별도 위키가 없어도 README·코드·설계 문서만으로 기록할 수 있다. 문서 속 원본 링크는 확인한 커밋에 고정했다.

## 지금 읽을 수 있는 프로젝트

- [노트버디](notebuddy.md): Python 상태 전이 함수가 웹 Pyodide와 Anna Worker에 연결되는 흐름. 게임 저장과 진화 조건도 공개 코드를 따라 설명한다.
- [옥션스팟 API](auction-spot.md): README의 서비스 구성을 출발점으로, 실제 이미지 업로드·로컬 저장·파일 제공 경로를 Java 코드에서 확인한다. 원본 프로젝트 위키 없이 작성한 사례다.
- [AGENT HUB](agent-hub.md): 로컬 CLI 호출, SQLite 작업 큐, 토론·검토 사본을 공개 코드의 경계에 따라 읽는다.
- [옥션스팟 프런트](auction-spot-front.md): Flutter 화면과 API·웹소켓·파일 업로드 경로.
- [Hermes 환경](hermes-env.md), [Hermes Agent Area](hermes-agent-area.md), [Hermes Team Hub](hermes-team-hub.md): 부트스트랩과 두 종류의 협업 화면.
- [Agent Drift Guard](agent-drift-guard.md): 현재 중단된 실험의 hook·세션 흐름.
- [Attendance PWA](attendance-pwa.md): 출퇴근 기록과 선택형 외부 연동.

## 기술 실험과 학습 기록

- [MSA Architecture](msa-architecture.md), [Spring Boot 예제](spring-boot.md), [Spring·React 템플릿](spring-react-template.md), [공항 주차 정보](airport-parking.md): Java·Spring의 서로 다른 실험 범위.
- [Flask·Leaflet 지도](flask-leaflet.md), [Flutter 프로필](flutter-profile.md): Python 웹 라우트와 Dart 화면 구조.
- [객체 추적](dl-object-tracking.md), [YOLO 객체 검출](dl-object-detecting.md), [차량 이미지 학습](dl-data-training.md), [Tesseract OCR](dl-tesseract.md): 읽은 코드 범위에 한정한 비전 실험.
- [Java 알고리즘 풀이](algorithms.md): 단일 파일의 기초 문제 풀이.

## 공개 자료의 역할

- [기술 블로그](kdkrkwhr.github.com.md), [정적 이력서](resume.md), [프로필 README](kdkrkwhr.md): 공개 표현물의 구현과 출처. 연락처와 검증되지 않은 개인 성과는 이 위키에 복제하지 않는다.
- [중앙 허브 구현](kdk-knowledge.md): 이 위키의 Markdown 원본·빌드·검증 흐름.
- [Spring AI fork](spring-ai.md), [Hermes Agent fork](hermes-agent.md), [AgentRadio fork](AgentRadio.md): upstream 코드와 확인된 fork 변경 범위를 구분한다.

## 다른 방향으로 읽기

- [Python 실행 경계](python-execution.md), [로컬 이미지 저장](image-storage.md), [로컬 작업 큐](local-queue.md)는 프로젝트의 기술 사용 사실을 연결한다.
- [개발 기준 참고](standards.md)는 별도 기준 저장소의 위치를 설명한다. 사례 프로젝트에 적용됐다는 근거는 아직 없다.
- [공개 저장소 목록과 작성 상태](repositories.md)는 28개 문서의 분석 범위와 fork 관계를 구분한다.
- [문서 갱신 절차](maintenance.md)는 공개 근거를 등록하고 문장을 대조하는 방법이다.

프로젝트를 소유하거나 공개했다는 사실만으로 개인 담당 범위·성과·선택 이유는 알 수 없다. 이 부분은 공개 가능한 기록이 생길 때까지 비워 둔다. 목차의 주제 묶음, 각 문서의 관련 개념, 그래프의 추출 요약은 Graphify가 이 위키 문서들에서 자동 추출한 결과이며 본문처럼 사람이 대조한 문장이 아니다. 사람이 등록한 편집 관계는 관계 데이터에서 `origin`으로 구분한다.
