---
{
  "id": "auction-spot",
  "type": "project",
  "order": 20,
  "summary": "동네 기반 실시간 경매 API에서 이미지 업로드가 실제로 저장·제공되는 경로",
  "sources": [
    "auction-readme",
    "auction-upload",
    "auction-storage",
    "auction-files"
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
# 옥션스팟 API: 문서의 기술 목록에서 실제 업로드 코드까지

옥션스팟 API는 동네 기반 실시간 경매 서비스의 공개 백엔드 저장소다. README에는 인증, 물품, 경매·입찰, 채팅, 신고, 이미지 업로드가 API 영역으로 제시돼 있다. 이 문서는 **이미지 파일이 들어와 어디에 저장되고 어떤 URL로 제공되는지**를 한 경로로 좁혀 읽는다. 프로젝트의 모든 API나 실제 운영 상태를 조사했다는 뜻은 아니다. [프로젝트 README](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

## 해결 대상과 공개된 범위

README는 경매 서비스에서 물품 이미지 업로드를 위한 `POST /api/v1/storage/upload`와 파일 조회를 위한 `GET /api/v1/files/**`를 설명한다. 또 설계 문서에 적힌 S3와 달리 **현재 이 API 저장소는 서버 로컬 디스크를 사용한다**고 직접 밝힌다. 이는 현재 구현에 대한 공개 사실이다. S3에서 로컬 저장으로 바꾼 이유나 어느 환경에 배포했는지는 README와 아래 코드만으로 알 수 없다. [업로드·저장 설명](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

이 저장소에 별도의 프로젝트 위키가 없어도 중앙 위키의 사례를 만들 수 있다. 이 글은 공개 README와 Java 파일만을 근거로 한다. 같은 흐름을 저장 경계 중심으로 다시 읽으려면 [로컬 이미지 저장](image-storage.md)을 보자.

## 공개 README가 보여 주는 구조

README는 Java 21과 Spring Boot 3.x를 전제로 REST 컨트롤러·서비스 계층·스케줄러를 설명한다. 실시간 경매 이벤트에는 WebSocket(STOMP), 영구 데이터에는 MySQL, 경매 큐와 입찰 상태 캐시에는 Redis, 인증에는 JWT가 적혀 있다. 이 목록은 **문서에 명시된 구성**이지 이 글에서 모든 모듈의 실행이나 외부 연동을 검증했다는 뜻이 아니다. [기술·API 개요](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

이미지 경로의 코드는 `infra/storage` 아래에 모여 있다. `LocalUploadController`는 HTTP 업로드 진입점, `LocalImageStorageService`는 파일 검사와 저장, `LocalFileWebConfig`는 저장 디렉터리를 정적 파일 URL에 매핑하는 역할을 한다. 이렇게 역할을 나누어 읽는 것은 파일의 실제 메서드와 연결을 요약한 것이다. 이 구조를 선택한 개인적 의도는 추론하지 않는다. [컨트롤러](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java) · [저장 서비스](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java) · [파일 제공 설정](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalFileWebConfig.java)

## 한 파일의 실행 흐름

1. `LocalUploadController.upload`는 multipart 요청의 `file`을 받아 저장 서비스에 넘기고 반환된 URL을 응답에 담는다. 이 메서드의 경로는 `/api/v1/storage/upload`다. [업로드 진입점](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java)
2. 저장 서비스는 빈 파일, 허용한 콘텐츠 유형, 설정된 최대 크기를 확인한다. 허용 유형은 JPEG·PNG·WebP·GIF다. 검사 후 UUID 기반 이름을 만들고 루트 아래 `items` 디렉터리에 복사한다. 여기서 읽은 것은 코드의 검사 순서이며 파일 내용 전체를 해석·검증한다고 말하지 않는다. [검사와 파일 저장](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java)
3. 서비스는 설정의 URL 접두와 `items/` 경로를 합쳐 요청 컨텍스트 기준 URL을 돌려준다. `LocalFileWebConfig`는 설정된 URL 패턴을 로컬 저장 루트의 리소스 위치에 연결한다. 반환 URL의 접근 정책과 실제 운영 환경은 이 두 파일만으로 단정하지 않는다. [URL 생성](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java) · [정적 제공 매핑](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalFileWebConfig.java)

## 기술과 다른 사례의 연결

이 경로에서 실제 읽은 코드는 Java와 Spring MVC의 컨트롤러·서비스·설정이다. MySQL·Redis·WebSocket은 README의 전체 API 구성으로 확인했지만, 이 이미지 경로의 직접 의존성이라고 쓰지 않는다. [기술 구성 원본](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

[로컬 이미지 저장](image-storage.md)은 저장 방식과 코드 근거를 기술 항목으로 모은 문서다. [노트버디](notebuddy.md)는 다른 언어·실행 환경에서 하나의 상태 전이 경계를 따라가는 사례다. 두 프로젝트가 같은 개발 기준을 적용했다는 주장은 하지 않는다.

## 확인 범위와 남은 질문

검토 기준은 `7c2d9496a5ae0f1dcd0345196483c2674ecff140` 커밋의 README와 세 Java 파일이다. 개인 담당 범위, S3와 다른 저장 방식의 선택 이유, 운영 배포 구조, 처리량·성과는 확인하지 못했다. 이를 채우려면 공개 가능한 결정 문서, 테스트 결과 또는 회고가 별도로 필요하다.
