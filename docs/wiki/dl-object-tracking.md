---
{"id":"dl-object-tracking","type":"project","order":70,"mapTitle":"객체 추적·차량 데이터 실험","summary":"TensorFlow Object Detection 계열 코드와 차량 라벨 변환 자료","sources":["dl-object-tracking-1","dl-object-tracking-2","dl-object-tracking-3"],"relations":[]}
---
# 객체 추적·차량 데이터 실험

**분석 기준:** `c00e0c9b9632b4a19497395b33208d3c9a08cc5f`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 자료와 출처

README는 Python 3.7, TensorFlow 1.13, OpenCV, SSD를 실험 환경으로 소개하고 외부 Object Detection·차량 계수 참고 자료를 밝힌다. `custom_vehicle_training` 아래에는 이미지·XML 라벨·CSV와 TensorFlow Object Detection 소스 트리가 함께 있다. 저장소에 코드가 존재한다는 것만으로 모든 검출기 구현을 개인 창작물이라 말할 수 없다.
[원본: `README.md`](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/README.md) [원본: `custom_vehicle_training/README.md`](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/README.md)

## 학습 데이터 변환 경로

`generate_tfrecord.py`는 CSV 라벨을 파일명별로 묶고 이미지를 읽어 좌표를 크기로 정규화한다. motorcycle·car·bus·truck을 번호로 매핑한 다음 TensorFlow Example을 직렬화해 TFRecord로 기록한다. 이 문서에서 실제 이미지나 학습 모델을 돌리지 않았다.
[원본: `custom_vehicle_training/generate_tfrecord.py`](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/generate_tfrecord.py)

## 추적 결과의 한계

README의 GIF와 참고 링크는 의도한 실험의 단서다. 여기서 실제 동영상 추적 정확도, 특정 모델의 학습 결과, 데이터 권리와 재현성을 확인한 것은 아니다.
[원본: `README.md`](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/README.md) [원본: `custom_vehicle_training/README.md`](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/README.md)

## 연결해서 읽기

[YOLO 객체 검출 예제](dl-object-detecting.md)는 다른 검출 방식의 코드이며, [차량 분류 학습](dl-data-training.md)은 별도 저장소다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
