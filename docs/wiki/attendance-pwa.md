---
{"id":"attendance-pwa","type":"project","order":31,"mapTitle":"출퇴근 체크 PWA","summary":"브라우저 저장 출퇴근 기록·퇴근 시각 계산·오프라인 캐시와 선택적 외부 연동","sources":["attendance-readme","attendance-app","attendance-config","attendance-sw","attendance-commute","attendance-news","attendance-ci"],"relations":[]}
---
# 출퇴근 체크 PWA: 로컬 기록과 선택적 연동의 경계

README는 서버 없이 설치해 쓰는 출퇴근 체크 PWA를 소개한다. 기본 계산은 출근 시각에서 8시간 근무와 1시간 점심을 더해 퇴근 가능 시각을 잡는 것이다. 실제 `js/app.js`는 체크인·체크아웃 기록과 설정을 브라우저 `localStorage`에서 읽고 쓰며, 알림·근무 진행률을 계산한다. 이 문서는 **개인의 출퇴근 기록 자체를 읽거나 공개하지 않았다.** [사용 안내](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/README.md) · [기록·시간 계산](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/app.js)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `4ee370fad304c5a1b142be72c5109d99a04ac0e3`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 보완 필요** 오프라인 캐시와 출퇴근 계산을 별도 파일로 뒀지만 중심 app.js가 기록·알림·네트워크·설정을 함께 다룬다. 기능 변경의 영향 범위가 넓다. [app.js 1–58행](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/app.js) [sw.js 29–76행](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/sw.js)
- **구현 품질 — 양호** Service Worker는 네트워크 우선·캐시 우선 경로를 분리하고 오프라인 응답을 명시한다. [sw.js 29–75행](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/sw.js)
- **운영 준비 — 위험** 선택 기능의 API 키와 생활 설정을 브라우저 localStorage의 같은 설정 객체에 보관한다. 해당 기능을 사용하는 공유 기기나 동일 오리진 스크립트 문제에 대비한 저장 범위 검토가 필요하다. 실제 사용·노출 여부는 미확인이다. [app.js의 기본 설정, 27–42행 및 loadSettings·saveSettings, 1128–1138행](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/app.js)
- **유지보수 — 보완 필요** 허용 네트워크·외부 연동 위치가 정적 설정 파일에 결합돼 환경을 바꾸려면 파일과 배포를 함께 관리해야 한다. 구체 값은 여기 옮기지 않는다. [config.js 12–25·35–53행](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/config.js)

**좋은 점:** 오프라인 동작 경로와 선택 연동의 설정 위치가 코드상 분명하다. **개선 우선순위:** P1 — 선택형 API 키의 장기 브라우저 저장을 재검토하고 민감 설정·일반 UI 설정을 분리한다. P2 — 큰 app.js를 기록·알림·연동 경계로 나눈다.

## 핵심 기록 흐름

`app.js`의 `loadRecords`·`saveRecords`는 날짜별 체크인·체크아웃을 로컬 저장한다. `calcLeaveTime`은 기본 근무 시간과 점심 시간을 합한 뒤 예상 퇴근 시각을 만든다. 네트워크 상태와 외근 상태를 고려하는 UI 경로도 있다. 이 로컬 상태는 각 브라우저에 한정되므로 자동 팀 DB 동기화라고 쓰지 않는다. [상태와 계산 코드](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/app.js)

`sw.js`는 HTML·JS·CSS·날씨·뉴스 데이터 요청에 네트워크 우선 방식을 쓰고 캐시를 대체 경로로 사용한다. 그 밖의 GET 자원은 캐시 우선이다. 오프라인 때 필요한 자산이 실제로 모두 준비되는지는 실행 검증하지 않았다. [서비스 워커](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/sw.js)

## README의 '서버 없음'을 읽는 범위

중심 출퇴근 기록은 브라우저에 있지만 부가 기능은 외부 요청을 사용할 수 있다. `app.js`에는 회사 네트워크 판단을 위한 공인 IP 조회, 사용자가 설정한 Google Sheet URL로 주간 기록을 보내는 함수가 있다. `commute-time.js`는 설정된 통근 경로 서비스를 조회하고, `news-brief.js`는 뉴스 데이터를 불러와 검색·읽음·핀 상태를 관리한다. 해당 기능의 사용 여부와 전송 대상은 설정과 사용자 동작에 따른다. **기본 로컬 저장과 선택적 네트워크 기능을 동일하게 '완전 오프라인'이라고 설명하지 않는다.** [앱 연동 코드](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/app.js) · [통근 모듈](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/commute-time.js) · [뉴스 모듈](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/js/news-brief.js) · [설정 구조](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/config.js)

공개 설정에는 네트워크 판단용 값과 지도 기본 위치가 들어 있다. 여기서는 기능과 제약만 기록하고 회사 IP, 위치값, 개인 이름·근무 내용은 재게시하지 않는다. [설정 파일](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/config.js)

## 배포 문서와 설정 차이

README는 Pages를 브랜치에서 켜는 절차를 안내한다. 현재 저장소의 `.github/workflows/pages.yml`에는 `main` 푸시에서 정적 파일을 모아 Pages artifact를 배포하는 Actions 경로가 정의돼 있다. 따라서 README의 절차를 현재 배포 설정의 유일한 근거로 삼지 않는다. 워크플로 정의를 읽은 것이며 이 문서에서 실제 배포 성공이나 앱의 알림 동작을 재검증한 것은 아니다. [README 배포 안내](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/README.md) · [Pages 워크플로](https://github.com/kdkrkwhr/attendance-pwa/blob/4ee370fad304c5a1b142be72c5109d99a04ac0e3/.github/workflows/pages.yml)

검토 기준은 `4ee370fad304c5a1b142be72c5109d99a04ac0e3`다. PWA 설치, 알림 권한, 외부 연동·실기기 동작은 실행하지 않았다. 개인 담당 역할, 사용 규모, 선택 이유·성과는 공개 코드만으로 확인할 수 없다.
