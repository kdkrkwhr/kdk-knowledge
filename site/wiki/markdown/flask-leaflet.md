---
{"id":"flask-leaflet","type":"project","order":68,"mapTitle":"Flask·Leaflet 지도 예제","summary":"Flask 라우트가 여러 Leaflet 지도 화면을 제공하는 실험","sources":["flask-leaflet-1","flask-leaflet-2","flask-leaflet-3","flask-leaflet-4"],"relations":[]}
---
# Flask·Leaflet 지도 예제

**분석 기준:** `cccfdf98ef0d6205ac007bcfcb338decb9ec7c50`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `cccfdf98ef0d6205ac007bcfcb338decb9ec7c50`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** Flask 라우트가 지도 예제별 HTML을 제공하고 CCTV 지도 스크립트가 위치·레이어 표시를 담당한다. [app.py 5–23행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/app.py) [cctvMap.js 47–111행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/static/js/cctvMap.js)
- **구현 품질 — 보완 필요** 지도 스크립트는 일부 타일을 HTTP로 요청하고 외부 지도 서비스 키를 클라이언트 코드에 직접 둔다. HTTPS 페이지에서는 지도 자산이 막히거나 키 사용 범위를 통제하기 어려울 수 있다. 키 값은 이 평가에 옮기지 않는다. [cctvMap.js 7–29행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/static/js/cctvMap.js)
- **운영 준비 — 위험** 직접 실행 경로가 debug 모드로 모든 네트워크 인터페이스에 바인딩한다. 공개 환경에서 그 방식으로 시작하면 개발용 디버거가 노출될 수 있다. 실제 공개 실행 여부는 확인하지 않았다. [app.py 25–26행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/app.py)
- **유지보수 — 보완 필요** HTML의 인라인 이벤트와 전역 지도 상태가 결합돼 화면을 확장할 때 이벤트 흐름을 추적하기 어렵다. [cctv_map.html 21–52행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/templates/page/cctv_map.html) [cctvMap.js 1–5행](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/static/js/cctvMap.js)

**좋은 점:** 각 지도 예제의 입구가 작고 CCTV 레이어 조작 흐름이 보인다. **개선 우선순위:** P1 — 외부 노출용 실행 설정에서 debug를 끄고 바인딩을 제한한다. P2 — 타일 HTTPS와 지도 키 제한·교체 정책을 정한다.

## 화면 라우팅

README는 바람·3D·CCTV·원형 마커 지도를 소개한다. `app.py`는 `/page/wind`, `/page/heatDraw`, `/page/cluster`, `/page/cctv`, `/page/3d` 요청을 각각 Jinja 템플릿으로 보낸다. 데이터 API 서버라기보다 지도 데모 화면을 제공하는 얇은 Flask 계층이다.
[원본: `README.md`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/README.md) [원본: `app.py`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/app.py)

## 브라우저 지도 동작

CCTV 화면은 Leaflet 지도와 별도 JavaScript를 로드한다. `cctvMap.js`에는 여러 타일 레이어, 현재 위치 요청, 마커·GeoJSON 상태가 있다. 지도 타일과 위치 접근은 브라우저·외부 제공자 조건에 의존한다.
[원본: `templates/page/cctv_map.html`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/templates/page/cctv_map.html) [원본: `static/js/cctvMap.js`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/static/js/cctvMap.js)

## 공개 소스의 경계

지도 코드에 공개 설정값과 서비스 URL이 있으나 이 문서는 키·정확한 기본 좌표를 복제하지 않는다. README의 그림은 결과 예시이고 현재 타일 제공자·브라우저에서 같은 화면이 열린다는 실행 증거는 아니다.
[원본: `README.md`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/README.md) [원본: `static/js/cctvMap.js`](https://github.com/kdkrkwhr/flask-leaflet/blob/cccfdf98ef0d6205ac007bcfcb338decb9ec7c50/static/js/cctvMap.js)

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
