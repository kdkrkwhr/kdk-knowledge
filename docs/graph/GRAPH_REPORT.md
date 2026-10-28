# Graph Report - wiki  (2026-10-28)

## Corpus Check
- Corpus is ~16,814 words - fits in a single context window. You may not need a graph.

## Summary
- 264 nodes · 491 edges · 11 communities
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Java·Spring 백엔드 실험
- 비전 실험과 저장소 색인
- Hermes 환경과 fork 경계
- 로컬 서버와 공개 화면의 경계
- 옥션스팟 경매 API·앱
- 로컬 에이전트 작업 허브
- 노트버디 상태 전이와 저장
- 지식 허브와 문서 기준
- 정적 공개 페이지
- 로컬 이미지 저장
- 지도 클라이언트와 키 노출

## God Nodes (most connected - your core abstractions)
1. `프로젝트에서 시작하는 위키 (index)` - 36 edges
2. `공개 저장소 목록과 문서 작성 상태` - 33 edges
3. `AGENT HUB` - 26 edges
4. `옥션스팟 API` - 22 edges
5. `Hermes Agent Area` - 19 edges
6. `Python` - 16 edges
7. `Engineering Standards: 선택형 개발 기준` - 16 edges
8. `Spring Boot 기술 예제 모음` - 14 edges
9. `출퇴근 체크 PWA` - 13 edges
10. `옥션스팟 Flutter` - 13 edges

## Surprising Connections (you probably didn't know these)
- `server/main.py (프로필·칸반·로그·브리프·미리보기·방송)` --semantically_similar_to--> `server.py (루프백 HTTP 서버·JSON API)`  [INFERRED] [semantically similar]
  hermes-agent-area.md → agent-hub.md
- `HubStore (js/store.js)` --semantically_similar_to--> `web/store.js (IndexedDB saves 저장소)`  [INFERRED] [semantically similar]
  hermes-team-hub.md → notebuddy.md
- `GET 경로 상태 변경·Origin 무검사 위험` --semantically_similar_to--> `SecurityConfig (일부 경로만 권한, 프레임 옵션 해제)`  [INFERRED] [semantically similar]
  hermes-team-hub.md → spring-react-template.md
- `재시작 실패 표시와 중복 전달 방지` --semantically_similar_to--> `GameApplication (공통 저장 오케스트레이션)`  [INFERRED] [semantically similar]
  local-queue.md → notebuddy.md
- `AgentRadio fork 참조` --conceptually_related_to--> `Python`  [INFERRED]
  AgentRadio.md → agent-hub.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hermes 에이전트 생태계 저장소군** — agent_drift_guard_agent_drift_guard, hermes_agent_area_hermes_agent_area, hermes_agent_hermes_agent, hermes_env_hermes_env, concept_hermes [EXTRACTED 1.00]
- **옥션스팟 입찰 요청-처리-이벤트 흐름 (클라이언트↔서버)** — auction_spot_front_auctionrepository, auction_spot_front_auctionwsclient, auction_spot_bidcommandservice, auction_spot_auctionlifecycleservice, auction_spot_redisauctioncache, concept_stomp [EXTRACTED 1.00]
- **차량 영상 딥러닝 실험군 (분류·검출·추적·OCR)** — dl_data_training_dl_data_training, dl_object_detecting_dl_object_detecting, dl_object_tracking_dl_object_tracking, dl_tesseract_dl_tesseract, concept_opencv, concept_tensorflow [INFERRED 0.85]
- **노트버디 transition 호출·저장 흐름** — notebuddy_web_worker, notebuddy_anna_game_worker, notebuddy_gameservice_invoke, notebuddy_gameapplication, notebuddy_transition, notebuddy_web_store [EXTRACTED 1.00]
- **Hermes Team Hub 로컬 실행형 구성** — hermes_team_hub_local_app, hermes_team_hub_team_hub_cli, hermes_team_hub_jsonl_model, hermes_team_hub_cli_allowlist [EXTRACTED 1.00]
- **kdk-knowledge 위키 빌드·검증 파이프라인** — kdk_knowledge_build_wiki, kdk_knowledge_validate, maintenance_sources_json, maintenance_add_project_procedure [EXTRACTED 1.00]

## Communities (11 total, 0 thin omitted)

### Community 0 - "Java·Spring 백엔드 실험"
Cohesion: 0.07
Nodes (36): 공항 주차 정보 실험, MainScheduler (1분 fixedDelay), RealTimeService.minuteScheduleF, Java 알고리즘 풀이 기록, TutorialSolution.java, GeoLocationService (Kakao 동 이름 변환), 백준(Baekjoon) 온라인 저지, Elasticsearch (+28 more)

### Community 1 - "비전 실험과 저장소 색인"
Cohesion: 0.10
Nodes (30): CNN (합성곱 신경망), Keras, 김동기 (kdkrkwhr), Maven, OpenCV, Python, RAG (벡터 저장소 통합), Spring AI (+22 more)

### Community 2 - "Hermes 환경과 fork 경계"
Cohesion: 0.07
Nodes (27): AgentRadio fork 참조, coral_multi_agent.py (Harbor 에이전트 실행 경로), resume_guard.py (중단 CLI 재개 래퍼), Bash 셸 스크립트, CLI 서브프로세스 호출, Coral, Coral Protocol, Hermes Agent (+19 more)

### Community 3 - "로컬 서버와 공개 화면의 경계"
Cohesion: 0.08
Nodes (23): app.js (loadRecords·saveRecords·calcLeaveTime), 출퇴근 체크 PWA, commute-time.js (통근 모듈), config.js (정적 설정), news-brief.js (뉴스 모듈), sw.js (Service Worker), Discord, FastAPI (+15 more)

### Community 4 - "옥션스팟 경매 API·앱"
Cohesion: 0.09
Nodes (29): KakaoSkillRestController (/api/kakao), 옥션스팟 API, AuctionLifecycleService (buildDailyQueue·종료), BidCommandService.placeBid, FcmNotificationService (로그 placeholder), app_router.dart, 옥션스팟 Flutter, AuctionRepository (/auctions REST) (+21 more)

### Community 5 - "로컬 에이전트 작업 허브"
Cohesion: 0.12
Nodes (21): agent-drift-guard, DriftGuardBuffer, format_injection, inject_at_boundary (Hermes 훅), SessionGuards, adapters.py (CLI 어댑터), AGENT HUB, engine.py (SQLite 지속 작업 큐) (+13 more)

### Community 6 - "노트버디 상태 전이와 저장"
Cohesion: 0.17
Nodes (15): Anna APS (ETag·요청 영수증), compare-and-set 리비전 갱신, IndexedDB, JavaScript Worker, Pyodide, anna game_worker.py (Anna Worker), engine/evolution.py 진화 규칙, ExecutionContext (규칙 데이터·템플릿·시각·난수원·ID 생성기) (+7 more)

### Community 7 - "지식 허브와 문서 기준"
Cohesion: 0.18
Nodes (12): Graphify, Markdown, scripts/build_wiki.py (kdk-knowledge), 중앙 지식 허브 구현 (kdk-knowledge), scripts/validate.py, 문서 작성과 갱신 (maintenance), docs/wiki/sources.json 근거 등록, scripts/build_wiki.py (engineering-standards 용어 위키 생성기) (+4 more)

### Community 8 - "정적 공개 페이지"
Cohesion: 0.22
Nodes (8): GitHub Pages, HTML·CSS 정적 페이지, Jekyll, Kramdown, 개인 기술 블로그 저장소 (kdkrkwhr.github.com), _data/projects.yml 프로젝트 목록 데이터, scripts/publish_blog.py 게시 확인 스크립트, 공개 이력서 페이지의 구현 (resume)

### Community 9 - "로컬 이미지 저장"
Cohesion: 0.29
Nodes (6): multipart 파일 업로드, S3, 로컬 이미지 저장: 요청에서 파일 URL까지, LocalFileWebConfig, LocalImageStorageService, LocalUploadController

### Community 10 - "지도 클라이언트와 키 노출"
Cohesion: 0.40
Nodes (3): GeoJSON, Leaflet, cctvMap.js (타일·위치·마커·GeoJSON)

## Knowledge Gaps
- **49 isolated node(s):** `coral_multi_agent.py (Harbor 에이전트 실행 경로)`, `resume_guard.py (중단 CLI 재개 래퍼)`, `format_injection`, `Claude Code`, `Codex CLI` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 75 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `프로젝트에서 시작하는 위키 (index)` connect `비전 실험과 저장소 색인` to `Java·Spring 백엔드 실험`, `Hermes 환경과 fork 경계`, `로컬 서버와 공개 화면의 경계`, `옥션스팟 경매 API·앱`, `로컬 에이전트 작업 허브`, `노트버디 상태 전이와 저장`, `지식 허브와 문서 기준`, `정적 공개 페이지`, `로컬 이미지 저장`?**
  _High betweenness centrality (0.367) - this node is a cross-community bridge._
- **What connects `coral_multi_agent.py (Harbor 에이전트 실행 경로)`, `resume_guard.py (중단 CLI 재개 래퍼)`, `format_injection` to the rest of the system?**
  _49 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Java·Spring 백엔드 실험` be split into smaller, more focused modules?**
  _Cohesion score 0.06755260243632337 - nodes in this community are weakly interconnected._
- **Why does `공개 저장소 목록과 문서 작성 상태` connect `비전 실험과 저장소 색인` to `Java·Spring 백엔드 실험`, `Hermes 환경과 fork 경계`, `로컬 서버와 공개 화면의 경계`, `옥션스팟 경매 API·앱`, `로컬 에이전트 작업 허브`, `노트버디 상태 전이와 저장`, `지식 허브와 문서 기준`, `정적 공개 페이지`?**
  _High betweenness centrality (0.277) - this node is a cross-community bridge._
- **Should `비전 실험과 저장소 색인` be split into smaller, more focused modules?**
  _Cohesion score 0.09759759759759759 - nodes in this community are weakly interconnected._
- **Why does `AGENT HUB` connect `로컬 에이전트 작업 허브` to `비전 실험과 저장소 색인`, `Hermes 환경과 fork 경계`, `로컬 서버와 공개 화면의 경계`, `지식 허브와 문서 기준`, `정적 공개 페이지`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Should `Hermes 환경과 fork 경계` be split into smaller, more focused modules?**
  _Cohesion score 0.07226890756302522 - nodes in this community are weakly interconnected._