---
{
  "id": "auction-spot",
  "type": "project",
  "order": 20,
  "summary": "동네 경매의 대기열·입찰·낙찰 흐름과 로컬 이미지 저장 구현",
  "sources": [
    "auction-readme",
    "auction-upload",
    "auction-storage",
    "auction-files",
    "auction-bid",
    "auction-lifecycle",
    "auction-cache",
    "auction-geo",
    "auction-fcm"
  ],
  "relations": [
    {
      "to": "image-storage",
      "label": "이미지를 API 서버의 로컬 디스크에 저장·제공",
      "evidence": [
        "auction-readme",
        "auction-upload",
        "auction-storage",
        "auction-files"
      ]
    }
  ],
  "mapTitle": "옥션스팟 API"
}
---
# 옥션스팟 API: 경매·입찰 흐름과 이미지 저장

옥션스팟 API는 동네 기반 실시간 경매 서비스의 공개 백엔드 저장소다. README에는 인증, 물품, 경매·입찰, 채팅, 신고, 이미지 업로드가 제시돼 있다. 이 문서는 **대기 중인 물품이 경매로 시작되고 입찰·종료·채팅으로 이어지는 중심 흐름**과 이미지 업로드 사례를 실제 Java 코드에서 나눠 살핀다. 모든 API의 실행이나 실제 운영 상태를 검증했다는 뜻은 아니다. [프로젝트 README](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `7c2d9496a5ae0f1dcd0345196483c2674ecff140`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 경매 대기열·시작·종료는 수명주기 서비스, 행 잠금 아래 입찰 검증·낙찰은 입찰 서비스로 나뉜다. 이미지 업로드도 별도 인프라 경계다. [AuctionLifecycleService.java 34–125행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java) · [BidCommandService.java 39–149행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/BidCommandService.java)
- **구현 품질 — 위험** 위치 변환은 키가 없을 때뿐 아니라 API 오류·빈 응답에도 요청 좌표와 무관한 고정 지역으로 대체한다. 동네 기준 경매에 쓰일 경우 잘못된 지역으로 분류될 수 있다. 실제 호출·배포 상태는 미확인이다. [GeoLocationService.resolve·stub 24–64행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/common/service/GeoLocationService.java)
- **운영 준비 — 보완 필요** FCM 서비스는 발송이 아닌 로그 placeholder이고 업로드 파일은 서버 로컬 디스크에 둔다. 실제 알림 전송이나 여러 인스턴스의 파일 공유를 보장하지 않는다. [FcmNotificationService.java 10–13행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/fcm/FcmNotificationService.java) · [LocalImageStorageService.java 35–43·78–93행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java)
- **유지보수 — 보완 필요** README의 Redis sorted-set 대기열 설명과 달리 읽은 코드에서는 DB의 queueOrder가 순서를 정하고 Redis는 선택적인 문자열 값 캐시다. 문서와 구현의 경계를 갱신해야 잘못된 운영 가정을 피할 수 있다. [AuctionLifecycleService.java 34–55행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java) · [RedisAuctionCache.java 12–33행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/RedisAuctionCache.java) · [README.md](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

**좋은 점:** 경매 시작·입찰·종료와 채팅 생성의 상태 전이가 코드에 명시되고, 입찰은 행 잠금 아래 제한을 검사한다. **개선 우선순위:** P1 — 위치 조회 실패를 고정 지역으로 성공처럼 돌리지 말고 미확인 상태로 전파해 잘못된 지역 분류를 막는다. P2 — 이미지 바이트 확인과 다중 서버 저장 정책, FCM placeholder·Redis 대기열 설명을 실제 구현과 맞춘다.

## 해결 대상과 공개된 범위

이 저장소의 중심 시나리오는 대기 중인 물품을 차례로 경매에 올리고, 유효한 입찰을 받아 종료 후 낙찰자와 채팅방을 연결하는 것이다. 이미지 업로드는 물품 등록에 필요한 별도 사례다. README는 업로드 `POST /api/v1/storage/upload`와 파일 조회 `GET /api/v1/files/**`를 설명하고, 설계 문서의 S3와 달리 **현재 API 저장소는 서버 로컬 디스크를 사용한다**고 밝힌다. 저장 방식을 바꾼 이유나 배포 환경은 확인하지 못했다. [경매 수명주기 34–125행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java) · [입찰 처리 39–149행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/BidCommandService.java) · [업로드·저장 README](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

이 저장소에 별도의 프로젝트 위키가 없어도 중앙 위키의 사례를 만들 수 있다. 이 글은 공개 README와 Java 파일만을 근거로 한다. 같은 흐름을 저장 경계 중심으로 다시 읽으려면 [로컬 이미지 저장](image-storage.md)을 보자.

## 공개 README가 보여 주는 구조

README는 Java 21과 Spring Boot 3.x를 전제로 REST 컨트롤러·서비스 계층·스케줄러를 설명한다. 실시간 경매 이벤트에는 WebSocket(STOMP), 영구 데이터에는 MySQL, 경매 큐와 입찰 상태 캐시에는 Redis, 인증에는 JWT가 적혀 있다. 다만 **읽은 구현에서 대기 순서는 DB의 queueOrder**이고, 선택적 Redis 구성은 현재 가격과 종료 시각을 문자열 값으로 보관한다. README의 Sorted Set 큐를 이 커밋의 실제 구현으로 단정하지 않는다. 모든 외부 연동의 실행도 확인하지 않았다. [기술·API 개요](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md) · [대기 순서 34–55행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java) · [Redis 값 캐시 12–33행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/RedisAuctionCache.java)

이미지 경로의 코드는 `infra/storage` 아래에 모여 있다. `LocalUploadController`는 HTTP 업로드 진입점, `LocalImageStorageService`는 파일 검사와 저장, `LocalFileWebConfig`는 저장 디렉터리를 정적 파일 URL에 매핑하는 역할을 한다. 이렇게 역할을 나누어 읽는 것은 파일의 실제 메서드와 연결을 요약한 것이다. 이 구조를 선택한 개인적 의도는 추론하지 않는다. [컨트롤러](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java) · [저장 서비스](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java) · [파일 제공 설정](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalFileWebConfig.java)

## 대기열에서 낙찰까지

1. `AuctionLifecycleService.buildDailyQueue`는 대기 중이고 물품 상태가 queued인 경매를 생성 시각순으로 정렬해 DB 엔터티의 `queueOrder`를 매긴다. 활성 경매가 없을 때 다음 대기 건을 시작하고 종료 시각을 현재로부터 5분으로 정한다. [AuctionLifecycleService.java 34–68행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java)
2. `BidCommandService.placeBid`는 경매 행을 잠가 활성 상태와 본인 물품·현재 선두 입찰자 여부를 확인한다. 기준 가격보다 높고 차액이 500원 단위인 입찰만 저장한다. 종료가 입찰 시각에서 60초보다 빠르면 종료 시각을 늘리며, 즉시 구매 가격에 도달하면 낙찰·채팅방 생성으로 끝낸다. 이는 코드 경로의 규칙이지 동시 사용자 환경에서의 처리량 검증은 아니다. [BidCommandService.java 39–149행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/BidCommandService.java)
3. 종료 시각이 지난 경매는 수명주기 서비스가 마무리한다. 입찰이 없으면 유찰 상태로, 있으면 최고 가격의 낙찰 입찰과 채팅방을 만들고 종료 이벤트를 전파한다. Redis 값 캐시는 있으면 갱신·삭제하는 보조 경로다. [AuctionLifecycleService.java 70–125행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/AuctionLifecycleService.java) · [RedisAuctionCache.java 17–33행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/RedisAuctionCache.java)

지역 조회는 Kakao 응답을 읽어 동 이름을 만드는 경로가 있으나 키 부재뿐 아니라 빈 응답·오류에서도 고정 지역을 돌려준다. FCM 서비스는 현재 실제 발송 대신 로그를 남기는 placeholder다. 따라서 README에 나열된 외부 기능을 모두 완료된 통합으로 읽으면 안 된다. [GeoLocationService.java 24–64행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/common/service/GeoLocationService.java) · [FcmNotificationService.java 10–13행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/fcm/FcmNotificationService.java)

## 이미지 업로드 실행 흐름

1. `LocalUploadController.upload`는 multipart 요청의 `file`을 받아 저장 서비스에 넘기고 반환된 URL을 응답에 담는다. 이 메서드의 경로는 `/api/v1/storage/upload`다. [업로드 진입점](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java)
2. 저장 서비스는 빈 파일, 허용한 콘텐츠 유형, 설정된 최대 크기를 확인한다. 허용 유형은 JPEG·PNG·WebP·GIF다. 검사 후 UUID 기반 이름을 만들고 루트 아래 `items` 디렉터리에 복사한다. 여기서 읽은 것은 코드의 검사 순서이며 파일 내용 전체를 해석·검증한다고 말하지 않는다. [검사와 파일 저장](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java)
3. 서비스는 설정의 URL 접두와 `items/` 경로를 합쳐 요청 컨텍스트 기준 URL을 돌려준다. `LocalFileWebConfig`는 설정된 URL 패턴을 로컬 저장 루트의 리소스 위치에 연결한다. 반환 URL의 접근 정책과 실제 운영 환경은 이 두 파일만으로 단정하지 않는다. [URL 생성](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java) · [정적 제공 매핑](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalFileWebConfig.java)

## 기술과 다른 사례의 연결

입찰 경로에서는 Java·Spring의 트랜잭션과 영속 경매 엔터티, 선택적 Redis 캐시·WebSocket 발행을 확인했다. 이미지 경로는 Spring MVC 컨트롤러·저장 서비스·정적 매핑이다. README의 전체 기술 목록과 각 흐름의 직접 의존성을 구분한다. [입찰 서비스 39–117행](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/domain/auction/service/BidCommandService.java) · [이미지 저장 서비스](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java)

[로컬 이미지 저장](image-storage.md)은 저장 방식과 코드 근거를 기술 항목으로 모은 문서다. [노트버디](notebuddy.md)는 다른 언어·실행 환경에서 하나의 상태 전이 경계를 따라가는 사례다. 두 프로젝트가 같은 개발 기준을 적용했다는 주장은 하지 않는다.

## 확인 범위와 남은 질문

검토 기준은 `7c2d9496a5ae0f1dcd0345196483c2674ecff140` 커밋의 README와 위에서 연결한 경매·지역·알림·저장 Java 파일이다. 개인 담당 범위, 저장 방식 선택 이유, 실제 배포 구조, 처리량·성과는 확인하지 못했다. 이를 채우려면 공개 가능한 결정 문서나 회고가 별도로 필요하다.
