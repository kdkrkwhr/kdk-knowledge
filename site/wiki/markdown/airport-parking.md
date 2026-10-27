---
{"id":"airport-parking","type":"project","order":67,"mapTitle":"공항 주차 정보 실험","summary":"공개 API XML 수집을 예약 실행하고 Redis와 Kakao 응답 경로를 둔 Spring 프로젝트","sources":["airport-parking-1","airport-parking-2","airport-parking-3","airport-parking-4"],"relations":[{"to":"spring-boot","label":"Spring Boot로 작성한 주차 정보 실험","evidence":["airport-parking-1"]}]}
---
# 공항 주차 정보 실험

**분석 기준:** `8ff191956a0a8a7746f511810a798754375903e2`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 데이터 수집 경로

`MainScheduler`는 1분 간격 fixedDelay로 `RealTimeService.minuteScheduleF`를 호출한다. 서비스는 로컬 JSON의 공항 코드를 순회하며 외부 주차 API XML을 읽고 주차장명·전체면수·점유면수 등을 파싱한다. 이 API 호출에는 설정된 키가 필요하지만 이 문서는 키나 결과 데이터를 공개하지 않는다.
[원본: `src/main/java/com/kdk/scheduler/MainScheduler.java`](https://github.com/kdkrkwhr/airport-parking/blob/8ff191956a0a8a7746f511810a798754375903e2/src/main/java/com/kdk/scheduler/MainScheduler.java) [원본: `src/main/java/com/kdk/service/RealTimeService.java`](https://github.com/kdkrkwhr/airport-parking/blob/8ff191956a0a8a7746f511810a798754375903e2/src/main/java/com/kdk/service/RealTimeService.java)

## 구현에서 확인한 제약

파싱한 `apiData`를 순회하지만 현재 Redis 저장 호출에는 `apiData`가 아니라 입력 JSON의 `data.toJSONString()`이 전달된다. 또 스케줄 메서드의 예외 catch는 비어 있다. 따라서 주차 잔여석이 Redis에 정확히 저장된다고 단정할 수 없다.
[원본: `src/main/java/com/kdk/service/RealTimeService.java`](https://github.com/kdkrkwhr/airport-parking/blob/8ff191956a0a8a7746f511810a798754375903e2/src/main/java/com/kdk/service/RealTimeService.java)

`/api/kakao` GET 컨트롤러는 Redis 수집 결과 대신 classpath의 `test.json`을 읽어 JSON으로 반환한다. 이 API가 실시간 주차 조회와 연결됐다고 설명하지 않는다.
[원본: `src/main/java/com/kdk/controller/KakaoSkillRestController.java`](https://github.com/kdkrkwhr/airport-parking/blob/8ff191956a0a8a7746f511810a798754375903e2/src/main/java/com/kdk/controller/KakaoSkillRestController.java)

## 기술 범위

Gradle은 Spring Boot와 데이터 관련 의존성을 정의한다. 실제 API 응답·Redis 저장·카카오 연동은 설치나 실행 없이 확인할 수 없다.
[원본: `build.gradle`](https://github.com/kdkrkwhr/airport-parking/blob/8ff191956a0a8a7746f511810a798754375903e2/build.gradle)

## 연결해서 읽기

[MSA Architecture](msa-architecture.md)와는 별도의 Spring 실험이다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
