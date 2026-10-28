---
{"id":"dl-object-detecting","type":"project","order":71,"mapTitle":"YOLO v3 객체 검출 예제","summary":"OpenCV 프레임 전처리와 Keras YOLO 추론을 연결한 데모","sources":["dl-object-detecting-1","dl-object-detecting-2","dl-object-detecting-3","dl-object-detecting-4"],"relations":[{"to":"dl-object-tracking","label":"YOLO와 SSD라는 다른 검출 접근을 기록","evidence":["dl-object-detecting-1"]}]}
---
# YOLO v3 객체 검출 예제

**분석 기준:** `373223b39fdb1401a838cba5b3cf096bc612e71f`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `373223b39fdb1401a838cba5b3cf096bc612e71f`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 화면 입출력과 YOLO 전처리·예측·후처리 클래스를 나눴다. [demo.py 9–45행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py) [yolo_model.py 8–18행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/model/yolo_model.py)
- **구현 품질 — 보완 필요** 동영상 읽기가 끝나거나 열리지 않으면 같은 파일을 계속 다시 열고 반복문이 종료되지 않는다. 캡처 해제 경로도 없어 입력 오류에서 자원을 계속 사용할 수 있다. [demo.py의 detect_video, 47–66행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py)
- **운영 준비 — 미확인** 모델과 동영상 경로가 로컬 파일로 고정된 시각화 예제다. 상시 영상 서비스의 운영 준비도는 적용 대상이 아니다. [yolo_model.py 8–18행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/model/yolo_model.py) [demo.py 68–77행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py)
- **유지보수 — 보완 필요** 클래스 목록·모델·영상 경로를 코드에서 각각 지정하므로 자료 교체 시 수정 지점이 흩어진다. [demo.py 68–77행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py) [yolo_model.py 16–18행](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/model/yolo_model.py)

**좋은 점:** 예측 파이프라인이 함수로 분리돼 관찰하기 쉽다. **개선 우선순위:** P2 — EOF·열기 실패 시 종료 여부를 명시하고 캡처를 해제하면 멈추지 않는 데모 루프를 피할 수 있다.

## 입력에서 표시까지

`demo.py`는 비디오 프레임을 416×416으로 리사이즈·정규화해 `YOLO.predict`에 전달한다. 반환된 상자·클래스·점수를 이미지 위에 그리며 창에서 프레임을 반복 출력한다. 비디오 파일 경로는 코드에 고정돼 있어 일반 CLI 앱으로 포장된 것은 아니다.
[원본: `demo.py`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py)

`model/yolo_model.py`는 YOLO 추론과 후보 상자 계산을, `model/darknet53.py`는 네트워크 구성을 담는다. README는 YOLO v3, TensorFlow GPU, Keras, OpenCV 환경을 기술한다.
[원본: `model/yolo_model.py`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/model/yolo_model.py) [원본: `model/darknet53.py`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/model/darknet53.py) [원본: `README.md`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/README.md)

## 검증과 기여 경계

README의 이미지와 모델 구조가 이 커밋에서 실제 학습된 가중치·정확도·실시간 성능을 증명하지는 않는다. 공개 LICENSE와 외부 알고리즘의 존재를 고려해 YOLO 자체 개발 성과라고 쓰지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/README.md) [원본: `demo.py`](https://github.com/kdkrkwhr/dl-object-detecting/blob/373223b39fdb1401a838cba5b3cf096bc612e71f/demo.py)

## 연결해서 읽기

[객체 추적·차량 데이터 실험](dl-object-tracking.md)은 SSD와 데이터 준비를 다룬다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
