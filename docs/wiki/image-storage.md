---
{
  "id": "image-storage",
  "type": "implementation",
  "order": 40,
  "summary": "옥션스팟 API의 multipart 업로드부터 로컬 파일 URL까지 확인한 구현",
  "sources": [
    "auction-readme",
    "auction-upload",
    "auction-storage",
    "auction-files"
  ],
  "relations": [],
  "mapTitle": "로컬 이미지 저장"
}
---
# 로컬 이미지 저장: 요청에서 파일 URL까지

[옥션스팟 API](auction-spot.md)의 공개 README는 문서의 S3 설계와 달리 현재 API가 **로컬 디스크**를 사용한다고 밝힌다. 이 문서는 그 설명에 연결되는 Java 파일 세 개를 읽은 결과다. [프로젝트 README](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/README.md)

## 코드에서 확인한 경로

1. `LocalUploadController`는 multipart 파일을 받아 서비스에 전달하고 저장 URL을 응답한다. [컨트롤러](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java)
2. `LocalImageStorageService`는 빈 파일, 콘텐츠 유형, 최대 크기를 검사한다. 허용 유형은 JPEG·PNG·WebP·GIF다. `items` 아래에 UUID 이름으로 복사한다. [저장 서비스](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalImageStorageService.java)
3. `LocalFileWebConfig`는 설정된 URL 패턴을 로컬 저장 루트에 매핑한다. 서비스가 만든 URL과 이 매핑을 함께 봐야 조회 경로가 보인다. [파일 제공 설정](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalFileWebConfig.java)

이것은 코드가 보여 주는 저장·제공 경로다. MIME 검사만으로 파일 내용 전체의 안전성을 확정할 수 없고, 파일 URL의 운영 접근 제어·배포 구성을 이 세 파일만으로 확정하지 않는다. S3와 다르게 구현한 결정 이유나 측정된 성과도 아직 근거가 없다.
