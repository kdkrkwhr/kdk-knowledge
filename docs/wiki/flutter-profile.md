---
{"id":"flutter-profile","type":"project","order":69,"mapTitle":"Flutter 프로필 예제","summary":"Flutter 화면·라우트·반응형 섹션을 둔 프로필 앱","sources":["flutter-profile-1","flutter-profile-2","flutter-profile-3","flutter-profile-4","flutter-profile-5"],"relations":[{"to":"resume","label":"개인 프로필을 표현하는 별도 화면 구현","evidence":["flutter-profile-1"]}]}
---
# Flutter 프로필 예제

**분석 기준:** `9e396bbddaa0178e2ccb99bebdad2ac27b4726ea`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 진입과 라우팅

README는 Dart·Flutter 프로필 프로젝트이고 DevFolio을 참고했다고 밝힌다. `main.dart`는 URL path 전략을 설정하고 Provider를 주입해 홈·협업 문의·상세 화면의 라우트를 등록한다. 참조한 템플릿의 존재 때문에 전체 화면을 독자 설계·구현이라고 단정하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/flutter-profile/blob/9e396bbddaa0178e2ccb99bebdad2ac27b4726ea/README.md) [원본: `lib/main.dart`](https://github.com/kdkrkwhr/flutter-profile/blob/9e396bbddaa0178e2ccb99bebdad2ac27b4726ea/lib/main.dart)

## 화면 구조

포트폴리오 섹션은 `responsive_builder`의 `ScreenTypeLayout`으로 모바일·태블릿 화면을 선택한다. 공개 코드에 프로필 문구와 연락 링크가 있지만 이 위키는 연락처나 개인 이력을 재게시하지 않는다.
[원본: `lib/sections/portfolio/portfolio.dart`](https://github.com/kdkrkwhr/flutter-profile/blob/9e396bbddaa0178e2ccb99bebdad2ac27b4726ea/lib/sections/portfolio/portfolio.dart) [원본: `pubspec.yaml`](https://github.com/kdkrkwhr/flutter-profile/blob/9e396bbddaa0178e2ccb99bebdad2ac27b4726ea/pubspec.yaml)

## 검증 한계

`test/widget_test.dart`는 Flutter 기본 위젯 테스트 형태로 보인다. 테스트 파일이 있다는 사실과 현재 프로필의 모든 라우트·반응형 화면이 정상 동작한다는 주장은 다르다.
[원본: `test/widget_test.dart`](https://github.com/kdkrkwhr/flutter-profile/blob/9e396bbddaa0178e2ccb99bebdad2ac27b4726ea/test/widget_test.dart)

## 연결해서 읽기

정적 이력서 페이지 [resume](resume.md)와 다른 Flutter 구현이다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
