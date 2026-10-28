---
{"id":"dl-object-tracking","type":"project","order":70,"mapTitle":"객체 추적·차량 데이터 실험","summary":"TensorFlow Object Detection 계열 코드와 차량 라벨 변환 자료","sources":["dl-object-tracking-1","dl-object-tracking-2","dl-object-tracking-3"],"relations":[]}
---
# 객체 추적·차량 데이터 실험

**분석 기준:** `c00e0c9b9632b4a19497395b33208d3c9a08cc5f`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `c00e0c9b9632b4a19497395b33208d3c9a08cc5f`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 미확인** 하위 README가 외부 TensorFlow Object Counting API 기반 예제이며 아직 구성 중이라고 밝힌다. 완성된 추적 서비스 구조를 이 파일들만으로 평가할 수 없다. [custom_vehicle_training/README.md 1–8행](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/README.md)
- **구현 품질 — 보완 필요** 클래스 변환 함수가 네 라벨 밖의 값에서 숫자 대신 None을 돌려준다. 데이터 변환 단계에서 잘못된 라벨이 조용히 넘어갈 수 있다. [generate_tfrecord.py의 class_text_to_int, 29–40·65–85행](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/generate_tfrecord.py)
- **운영 준비 — 미확인** README가 학습 진행 중이라고 쓰고 변환 스크립트는 외부 object_detection 패키지·로컬 이미지 폴더를 전제한다. 서비스 운영 점수로 재단하지 않는다. [custom_vehicle_training/README.md 4–8·18–28행](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/README.md) [generate_tfrecord.py 90–101행](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/generate_tfrecord.py)
- **유지보수 — 보완 필요** 라벨 ID와 이미지 위치가 코드에 고정돼 다른 데이터셋을 가져올 때 수동 변경이 필요하다. [generate_tfrecord.py 29–40·90–96행](https://github.com/kdkrkwhr/dl-object-tracking/blob/c00e0c9b9632b4a19497395b33208d3c9a08cc5f/custom_vehicle_training/generate_tfrecord.py)

**좋은 점:** CSV의 이미지별 객체를 묶어 TFRecord로 만드는 변환 흐름은 분리돼 있다. **개선 우선순위:** P2 — 허용 라벨을 명시하고 모르는 라벨은 즉시 오류로 처리하면 잘못된 학습 입력을 앞단에서 찾을 수 있다.

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
