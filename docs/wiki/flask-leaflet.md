---
{"id":"flask-leaflet","type":"project","order":68,"mapTitle":"Flask·Leaflet 지도 예제","summary":"Flask 라우트가 여러 Leaflet 지도 화면을 제공하는 실험","sources":["flask-leaflet-1","flask-leaflet-2","flask-leaflet-3","flask-leaflet-4"],"relations":[]}
---
# Flask·Leaflet 지도 예제

**분석 기준:** `cccfdf98ef0d6205ac007bcfcb338decb9ec7c50`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

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
