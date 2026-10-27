---
{"id":"auction-spot-front","type":"project","order":22,"mapTitle":"옥션스팟 Flutter","summary":"옥션스팟의 Flutter 클라이언트가 REST·STOMP·이미지 업로드를 호출하는 경로","sources":["front-readme","front-main","front-router","front-dio","front-auction","front-ws","front-upload","front-pubspec","front-starter","front-constants","auction-upload"],"relations":[{"to":"auction-spot","label":"이미지 업로드 요청 경로가 API 컨트롤러와 대응","evidence":["front-upload","front-constants","auction-upload"]}]}
---
# 옥션스팟 Flutter: 경매 화면에서 API와 실시간 채널까지

이 저장소는 옥션스팟의 Flutter 클라이언트 코드를 담는다. **루트 README는 기본 Flutter 시작 문구**라 서비스 기능의 증거로 쓰기 어렵다. 실제 구현은 루트 `lib/`와 `pubspec.yaml`에서 확인했다. 저장소 안의 `auction_spot/lib/main.dart`에는 별도의 기본 카운터 예제가 남아 있다. 어느 디렉터리를 실제 빌드·배포했는지는 정적 파일만으로 확정할 수 없으므로, 아래는 **루트 앱 코드의 흐름**이다. [루트 README](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/README.md) · [루트 main.dart](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/main.dart) · [내부 시작 예제](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/auction_spot/lib/main.dart)

## 앱 진입과 화면 경로

루트 `main.dart`는 Flutter 바인딩을 준비하고 Firebase 초기화를 시도한 뒤 Riverpod `ProviderScope`에서 앱을 시작한다. 초기화 오류는 debug 모드에서 기록하고 계속 진행한다. `app_router.dart`는 splash·onboarding·login과 홈, 물품 등록, 채팅, 마이페이지를 배치하며 `/item/:itemId`, `/auction/:auctionId`, `/chat/:roomId` 상세 경로를 둔다. 이는 화면 이동을 위한 코드 구조이지 각 기능의 실제 서비스 성공을 검증했다는 뜻은 아니다. [앱 진입](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/main.dart) · [라우터](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/core/router/app_router.dart)

## REST 요청과 입찰 이벤트

`DioClient`는 API 기본 URL과 10초 연결·응답 제한을 설정한다. 요청 인터셉터가 저장된 액세스 토큰을 Bearer 헤더에 넣고, 401 응답에서 리프레시 토큰이 있으면 갱신 뒤 원래 요청을 재시도한다. 로그 인터셉터는 요청·응답 본문 출력으로 설정돼 있다. 이 코드만으로 토큰 갱신 동시성이나 운영 로그의 안전성을 보장할 수 없다. [HTTP 클라이언트](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/core/network/dio_client.dart)

`AuctionRepository`는 오늘의 경매, 상세, 입찰 목록·제출, 결과를 `/auctions/...` REST 경로로 요청하고 응답 모델로 변환한다. `AuctionWsClient`는 STOMP로 `/topic/auctions/{auctionId}`를 구독해 이벤트 스트림에 전달하며 3초 재연결 간격을 설정한다. 경매 결과와 실시간 이벤트가 화면에 어떻게 합쳐지는지는 이 두 파일만으로 모두 확인하지 않았다. [REST 경매 저장소](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/features/auction/data/auction_repository.dart) · [STOMP 클라이언트](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/features/auction/data/auction_ws_client.dart)

## 이미지 업로드와 백엔드 연결

`StorageRepository.uploadItemImage`는 파일 바이트를 multipart `file` 필드에 담아 `/storage/upload`로 POST하고 응답의 `url`을 돌려준다. 파일 확장자로 JPEG·PNG·WebP·GIF MIME을 정한다. `AppConstants.baseUrl`은 로컬 API의 `/api/v1`이고 Android 에뮬레이터에서는 호스트 주소를 `10.0.2.2`로 바꾼다. 따라서 클라이언트가 만드는 전체 경로는 [옥션스팟 API](auction-spot.md)의 업로드 컨트롤러 경로와 대응한다. **요청·응답 계약의 정적 대응**을 확인한 것이며 두 저장소의 실제 통합 실행을 확인한 것은 아니다. [업로드 호출](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/features/storage/data/storage_repository.dart) · [API 주소](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/lib/core/constants/app_constants.dart) · [서버 컨트롤러](https://github.com/kdkrkwhr/auction-spot-api/blob/7c2d9496a5ae0f1dcd0345196483c2674ecff140/src/main/java/com/auctionspot/infra/storage/LocalUploadController.java)

## 확인한 기술과 한계

루트 `pubspec.yaml`에는 Flutter·Riverpod·go_router·Dio·secure storage·geolocator·STOMP·Firebase Messaging 의존성이 선언돼 있다. 선언은 실제 사용 여부를 각각 증명하지 않으므로 위에서 읽은 코드의 Flutter, Riverpod, Dio, STOMP만 구체적 흐름으로 설명했다. [루트 의존성](https://github.com/kdkrkwhr/auction-spot-front/blob/abb91bc2abe406e821c55f362e9f209ea61c2db9/pubspec.yaml)

검토 기준은 `abb91bc2abe406e821c55f362e9f209ea61c2db9`의 위 파일이다. 앱 빌드, 서버 통합, 입찰 실시간 전달, 푸시 수신은 실행하지 않았다. 개인 담당 범위와 기술 선택 이유·성과도 확인하지 못했다. 루트 README와 실제 앱 코드의 정보량 차이를 남겨 향후 문서 갱신 때 확인할 수 있게 한다.
