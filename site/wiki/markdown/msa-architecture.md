---
{"id":"msa-architecture","type":"project","order":64,"mapTitle":"MSA Architecture 실험","summary":"Eureka 등록·Zuul 경로 분기와 Flask 서비스를 묶은 실험","sources":["msa-architecture-1","msa-architecture-2","msa-architecture-3","msa-architecture-4","msa-architecture-5"],"relations":[{"to":"spring-boot","label":"Spring Boot 기반 서비스 발견과 게이트웨이 실험","evidence":["msa-architecture-1"]}]}
---
# MSA Architecture 실험

**분석 기준:** `daab901385eda3f6cc0c5c7cafb8506affbac1b1`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `daab901385eda3f6cc0c5c7cafb8506affbac1b1`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** Eureka 서버, Zuul 게이트웨이, Spring·Flask 예제를 별도 모듈로 나눠 서비스 발견 실험을 읽기 쉽다. [Eureka 설정 1–13행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka/src/main/resources/application.yml) [게이트웨이 설정 8–23행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/resources/application.yml)
- **구현 품질 — 보완 필요** Flask의 URL 수집 경로가 요청의 URL·태그를 그대로 크롤러에 넘긴다. 입력 범위와 오류 응답 정책은 이 파일에서 드러나지 않는다. 외부 노출 시 허용 대상 검토가 필요하다. [flask app.py 17–30행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/flask-eureka-zuul-service/app.py)
- **운영 준비 — 미확인** 게이트웨이 목적지가 localhost 포트로 고정된 실험 구성이다. 분산 운영 준비도를 평가할 서비스라고 보지 않으며 실제 배포는 확인하지 않았다. [Zuul application.yml 8–23행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/resources/application.yml)
- **유지보수 — 보완 필요** 여러 서비스의 포트와 주소를 개별 설정에 반복 입력해야 다른 환경에서 재현할 수 있다. [Eureka application.yml 5–13행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka/src/main/resources/application.yml) [Zuul application.yml 5–23행](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/resources/application.yml)

**좋은 점:** 라우팅과 서비스 발견의 실험 단위가 분명하다. **개선 우선순위:** P2 — 예제를 재사용할 때 URL 입력의 허용 범위와 환경별 주소 설정을 명시하면 예상치 못한 대상 호출과 재현 실패를 줄인다.

## 저장소의 구성

루트 README는 Spring Boot와 Eureka 서버·클라이언트를 실험 주제로 적는다. 실제 트리에는 Eureka 서버, 두 애플리케이션, 클라이언트, Zuul 게이트웨이, Flask 서비스가 각각 별도 디렉터리로 있다. 단일 완제품보다 서비스 발견과 라우팅을 조합한 학습용 구성으로 읽는 것이 정확하다.
[원본: `README.md`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/README.md) [원본: `spring-eureka/src/main/resources/application.yml`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka/src/main/resources/application.yml)

## 요청 흐름

Zuul 설정은 `/api/**`를 로컬 8101로, `/craw/**`를 8102로 보내고 Eureka 주소를 별도로 설정한다. 이 경로는 설정값으로 확인되지만 서비스 전체를 실제 기동해 동작을 증명하지는 않았다.
[원본: `spring-eureka-zuul/src/main/resources/application.yml`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/resources/application.yml)

Flask `app.py`는 시작 시 `py_eureka_client`로 서비스를 등록한다. GET `/craw/url`은 코드에 고정된 공개 GitHub 주소를 크롤링하지만, POST `/craw/get_data`는 요청 본문의 URL·태그를 `crawler_parsing`에 넘긴다. 두 경로의 입력 신뢰도가 다르므로 후자를 외부에 열기 전에는 입력 대상과 오류 응답을 정의해야 한다. `/craw/test`는 받은 파라미터를 응답에 돌려주는 예제다. 이는 코드 흐름의 정적 설명이지 보안·확장성 검증 결과는 아니다.
[원본: `flask-eureka-zuul-service/app.py`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/flask-eureka-zuul-service/app.py)

## 판단할 때의 경계

Zuul의 요청 전 필터는 모든 요청의 URI·메서드를 기록하는 예제이며 인증이나 대상 URL 검증을 수행하지 않는다. 공개 설정은 localhost 중심이어서 외부 환경의 서비스 발견, 장애 전환, 배포 자동화까지 확인할 수 없다.
[원본: `spring-eureka-zuul/src/main/java/com/kdk/filter/PreFilter.java`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/java/com/kdk/filter/PreFilter.java) [원본: `spring-eureka-zuul/src/main/resources/application.yml`](https://github.com/kdkrkwhr/msa-architecture/blob/daab901385eda3f6cc0c5c7cafb8506affbac1b1/spring-eureka-zuul/src/main/resources/application.yml)

## 연결해서 읽기

[Spring Boot 예제 모음](spring-boot.md)은 개별 기술 예제이고, 이 문서는 여러 서비스의 연결 구성을 다룬다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
