---
{"id":"repositories","type":"guide","order":60,"summary":"공개 저장소 28개의 범위와 위키 문서 작성 상태","sources":[],"relations":[]}
---
# 공개 저장소 목록과 문서 작성 상태

2026-10-27에 [공개 저장소 목록](https://github.com/kdkrkwhr?tab=repositories)에서 `kdkrkwhr` 계정의 공개 저장소 28개를 확인했다. 25개 non-fork와 3개 fork 모두 고정 커밋에서 실제 소스·설정 중 핵심 파일을 읽고, README가 있는 경우 안내와 대조해 문서를 작성했다. **정적 분석은 실행 검증이나 개인 기여 검증이 아니다.** 특히 큰 기술 모음과 upstream fork는 문서에 적힌 파일 범위만 조사했다. non-fork도 단독 저작을 뜻하지 않는다.

## 문서 작성 완료 · non-fork 25

- `notebook-pets` → [노트버디](notebuddy.md): README와 Python·JavaScript 파일을 고정 커밋에서 대조했다.
- `auction-spot-api` → [옥션스팟 API](auction-spot.md): README와 Java 이미지 저장 경로를 고정 커밋에서 대조했다.
- `agent-hub` → [AGENT HUB](agent-hub.md): README와 Python CLI·서버·작업 엔진·사본 코드를 고정 커밋에서 정적으로 대조했다.
- `auction-spot-front` → [옥션스팟 프런트](auction-spot-front.md): Dart 진입점·라우터·네트워크·저장소 코드를 대조했다.
- `hermes-env` → [Hermes 환경](hermes-env.md): 설치 안내와 부트스트랩·설정 파일을 대조했다.
- `hermes-agent-area` → [Hermes Agent Area](hermes-agent-area.md): 웹·서버·테스트 코드를 대조했다.
- `hermes-team-hub` → [Hermes Team Hub](hermes-team-hub.md): 정적 화면과 로컬 서버 코드를 대조했다.
- `agent-drift-guard` → [Agent Drift Guard](agent-drift-guard.md): 중단 상태와 hook·세션 코드를 대조했다.
- `engineering-standards` → [개발 기준 참고](standards.md): 현재 README·프로필·검증 코드를 대조했다.
- `attendance-pwa` → [Attendance PWA](attendance-pwa.md): 웹 앱·서비스 워커·설정을 대조했다.
- `msa-architecture` → [MSA Architecture](msa-architecture.md): Eureka·Zuul 설정과 Flask 진입점을 대조했다.
- `spring-boot` → [Spring Boot 예제 모음](spring-boot.md): 여러 독립 예제 중 크롤링·검색·FCM 코드를 대조했다.
- `spring-react-template` → [Spring·React 템플릿](spring-react-template.md): 백엔드 모듈과 React 시작 화면의 차이를 대조했다.
- `airport-parking` → [공항 주차 정보](airport-parking.md): API 수집·예약 실행·Redis 저장 코드의 경계를 대조했다.
- `flask-leaflet` → [Flask·Leaflet](flask-leaflet.md): Flask 라우트와 지도 화면 코드를 대조했다.
- `flutter-profile` → [Flutter 프로필](flutter-profile.md): Flutter 라우트·화면·위젯 테스트를 대조했다.
- `dl-object-tracking` → [객체 추적·차량 데이터](dl-object-tracking.md): README와 TFRecord 변환 코드를 대조했다.
- `dl-object-detecting` → [YOLO 객체 검출](dl-object-detecting.md): 프레임 전처리와 모델 파일을 대조했다.
- `dl-data-training` → [차량 이미지 학습](dl-data-training.md): 단일 Keras 파일을 대조했다.
- `dl-tesseract` → [Tesseract OCR](dl-tesseract.md): 영상 전처리와 OCR 코드를 대조했다.
- `algorithms` → [Java 알고리즘 풀이](algorithms.md): 단일 Java 파일을 대조했다.
- `kdkrkwhr.github.com` → [기술 블로그 저장소](kdkrkwhr.github.com.md): Jekyll 설정·게시 확인 코드를 대조했다.
- `resume` → [정적 이력서 구현](resume.md): HTML·CSS 게시 구조만 기록했다.
- `kdkrkwhr` → [프로필 README](kdkrkwhr.md): 공개 인덱스의 역할을 기록했다.
- `kdk-knowledge` → [중앙 허브 구현](kdk-knowledge.md): Markdown 빌드와 검증 흐름을 기록했다.

`agent-drift-guard`의 공개 README는 중단된 상태와 대체 경로를 설명하므로 현재 운영 프로젝트처럼 다루지 않는다. `resume`, 프로필, 웹사이트 자료를 살필 때 공개돼 있다는 이유만으로 연락처 등 불필요한 개인정보를 이 위키에 다시 싣지 않는다.

## Fork 문서 · 3

- [spring-ai](spring-ai.md) (원본: `spring-projects/spring-ai`): 기본 브랜치의 fork 고유 커밋 확인되지 않음.
- [hermes-agent](hermes-agent.md) (원본: `NousResearch/hermes-agent`): 기본 브랜치의 두 변경 커밋·파일 범위를 분리해 기록.
- [AgentRadio](AgentRadio.md) (원본: `Coral-Protocol/AgentRadio`): 기본 브랜치의 fork 고유 커밋 확인되지 않음.

fork 관계는 GitHub 저장소 메타데이터에서 확인했다. 기본 브랜치 비교만으로 다른 브랜치나 외부 PR 기여까지 배제할 수 없다. upstream README의 기능·성과를 fork 계정 소유자의 성과로 옮기지 않았다.

새 문서를 작성하는 순서와 공개 검증은 [문서 갱신 절차](maintenance.md)를 따른다.
