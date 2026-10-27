---
{"id":"spring-boot","type":"project","order":65,"mapTitle":"Spring Boot 기술 예제 모음","summary":"크롤링·Elasticsearch·FCM·Kafka 등 여러 독립 예제가 든 저장소","sources":["spring-boot-1","spring-boot-2","spring-boot-3","spring-boot-4","spring-boot-5","spring-boot-6"],"relations":[]}
---
# Spring Boot 기술 예제 모음

**분석 기준:** `b0a8b227af8ed65ef684a5950d0c97d42bf13d41`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 하나의 서비스가 아닌 예제 모음

README는 Spring Boot 기술 모음이라고 소개한다. 루트 아래에는 admin, crawling, Elasticsearch, FCM 클라이언트·서버, JPA, Kafka, MyBatis, Redis, Security 등 별도 Gradle 프로젝트가 있다. 따라서 이 저장소의 기능을 하나의 배포 서비스가 모두 제공한다고 읽지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/README.md) [원본: `spring-kafka/build.gradle`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/spring-kafka/build.gradle) [원본: `spring-security-jwt/build.gradle`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/spring-security-jwt/build.gradle)

## 대표 구현 두 개

크롤링 예제의 `CrawlerUtil.findByTag`는 Jsoup로 URL의 HTML을 가져와 지정 class의 텍스트 목록을 만든다. 네트워크 오류는 출력한 뒤 빈 결과를 돌릴 수 있다. 실제 대상 사이트의 응답이나 수집 정책은 별도 확인이 필요하다.
[원본: `spring-crawling/src/main/java/com/kdk/util/CrawlerUtil.java`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/spring-crawling/src/main/java/com/kdk/util/CrawlerUtil.java)

Elasticsearch 예제의 `BookService`는 저장소를 통한 책 문서 생성·삭제와 `ElasticsearchRestTemplate`의 `userName` 일치 검색을 분리한다. 코드가 표현하는 API 패턴이며 검색 정확도나 운영 인덱스 설계 결과는 아니다.
[원본: `spring-elasticsearch/src/main/java/com/kdk/service/BookService.java`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/spring-elasticsearch/src/main/java/com/kdk/service/BookService.java)

FCM 서버 예제에도 별도 서비스 코드가 있다. 알림 전송은 외부 FCM 설정과 자격 증명을 요구하므로 이 정적 검토에서 전달 성공을 주장하지 않는다.
[원본: `spring-fcm-server/src/main/java/com/kdk/service/FcmServerService.java`](https://github.com/kdkrkwhr/spring-boot/blob/b0a8b227af8ed65ef684a5950d0c97d42bf13d41/spring-fcm-server/src/main/java/com/kdk/service/FcmServerService.java)

## 연결해서 읽기

[MSA Architecture](msa-architecture.md)는 복수 서비스 라우팅 구성이고, [Spring·React 템플릿](spring-react-template.md)은 출발점 저장소다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
