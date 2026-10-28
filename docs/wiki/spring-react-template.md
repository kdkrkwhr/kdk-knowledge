---
{"id":"spring-react-template","type":"project","order":66,"mapTitle":"Spring·React 프로젝트 템플릿","summary":"Gradle 백엔드 골격과 React 시작 화면을 함께 둔 템플릿","sources":["spring-react-template-1","spring-react-template-2","spring-react-template-3","spring-react-template-4","spring-react-template-5","spring-react-template-6"],"relations":[{"to":"spring-boot","label":"Spring Boot 백엔드 골격을 포함","evidence":["spring-react-template-1"]}]}
---
# Spring·React 프로젝트 템플릿

**분석 기준:** `2624ccc506dcc914325bf0e2aa5442e7c4f89621`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `2624ccc506dcc914325bf0e2aa5442e7c4f89621`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 보완 필요** 백엔드는 API·공통·Redis·Kafka 등 모듈을 나눴지만 프런트는 기본 React 시작 화면으로 남아 두 층의 통합 경로가 보이지 않는다. [settings.gradle 6–11행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/settings.gradle) [App.js 1–26행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/src/App.js)
- **구현 품질 — 보완 필요** 보안 설정은 일부 경로만 권한을 요구하고 나머지는 모두 허용하며 프레임 옵션도 끈다. 템플릿을 실제 서비스에 재사용할 때 엔드포인트별 공개 범위를 다시 정해야 한다. [SecurityConfig.java 42–55행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/app/api-server/src/main/java/com/kdk/config/SecurityConfig.java)
- **운영 준비 — 미확인** 프로젝트 골격과 예시 화면이므로 완성된 서비스 운영 준비도는 적용하지 않는다. 현재 배포·사용도 확인하지 않았다. [App.js 5–24행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/src/App.js)
- **유지보수 — 보완 필요** 프런트 의존성이 예제 시점의 버전에 묶여 있고 백엔드 모듈도 많아 실제 사용 목적을 정한 뒤 필요한 것만 남기는 편이 낫다. [package.json 5–18행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/package.json) [settings.gradle 6–11행](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/settings.gradle)

**좋은 점:** 백엔드 관심사를 나눠 출발 구조를 탐색하기 쉽다. **개선 우선순위:** P1 — 서비스 재사용 전에 권한 기본값과 프레임 정책을 요구 기능에 맞게 재검토한다. P2 — 프런트·백 간 한 흐름을 정의해 템플릿의 실제 통합 경계를 보여 준다.

## 백엔드 모듈과 화면의 실제 상태

README는 Java 8, Spring Boot, React를 기본 환경으로 안내한다. `backend/settings.gradle`에는 API 서버, 공통, Redis·Kafka 라이브러리 모듈이 나열돼 있다. 다만 현재 `frontend/src/App.js`는 React 기본 시작 화면 그대로이므로 완성된 프런트 기능이라고 설명하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/README.md) [원본: `backend/settings.gradle`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/settings.gradle) [원본: `frontend/src/App.js`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/src/App.js) [원본: `frontend/package.json`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/package.json)

## 확인 가능한 웹 흐름

백엔드 `UserController`는 로그인 화면 진입·회원가입·로그아웃 URL을 제공한다. 회원가입 요청은 서비스에 위임하고, 로그아웃은 remember-me 쿠키와 Spring Security 컨텍스트를 지운다. `SecurityConfig`는 인증 관련 설정을 둔다. 이는 백엔드 소스의 경로일 뿐 프런트 시작 화면에서 실제 호출한다는 근거는 없다.
[원본: `backend/app/api-server/src/main/java/com/kdk/web/UserController.java`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/app/api-server/src/main/java/com/kdk/web/UserController.java) [원본: `backend/app/api-server/src/main/java/com/kdk/config/SecurityConfig.java`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/backend/app/api-server/src/main/java/com/kdk/config/SecurityConfig.java)

## 재사용 시 주의

의존성 선언과 예제 코드는 기반 구조를 보여 주지만, 현재 서비스에 바로 적용 가능한 보안 수준이나 최신 패키지 호환성은 검증하지 않았다. README의 설치 지시와 소스가 표현하는 구현 범위를 분리해서 읽어야 한다.
[원본: `README.md`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/README.md) [원본: `frontend/package.json`](https://github.com/kdkrkwhr/spring-react-template/blob/2624ccc506dcc914325bf0e2aa5442e7c4f89621/frontend/package.json)

## 연결해서 읽기

[Spring Boot 기술 예제 모음](spring-boot.md)과 용도가 다르며 [개발 기준](standards.md)을 실제 적용했다는 근거는 없다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
