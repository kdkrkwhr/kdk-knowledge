---
{"id":"dl-object-detecting","type":"project","order":71,"mapTitle":"YOLO v3 객체 검출 예제","summary":"OpenCV 프레임 전처리와 Keras YOLO 추론을 연결한 데모","sources":["dl-object-detecting-1","dl-object-detecting-2","dl-object-detecting-3","dl-object-detecting-4"],"relations":[{"to":"dl-object-tracking","label":"YOLO와 SSD라는 다른 검출 접근을 기록","evidence":["dl-object-detecting-1"]}]}
---
# YOLO v3 객체 검출 예제

**분석 기준:** `373223b39fdb1401a838cba5b3cf096bc612e71f`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

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
