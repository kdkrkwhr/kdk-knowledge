---
{"id":"dl-data-training","type":"project","order":72,"mapTitle":"차량 이미지 분류 학습 스크립트","summary":"단일 Keras 파일에 적힌 CNN 구성과 폴더 입력 학습 흐름","sources":["dl-data-training-1"],"relations":[]}
---
# 차량 이미지 분류 학습 스크립트

**분석 기준:** `a6b6af0142a3d57ebeac89c38c89d9dadd614c59`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `a6b6af0142a3d57ebeac89c38c89d9dadd614c59`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 단일 학습 스크립트에서 이미지 전처리·CNN 구성·학습·저장을 순서대로 볼 수 있어 실험 기록 목적에는 맞다. [train_car.py 18–83행](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)
- **구현 품질 — 보완 필요** 학습 epoch는 60인데 그래프용 epoch 열은 30개로 만든다. 결과 표의 뒷부분이 비거나 맞지 않을 수 있어 학습 곡선 해석을 흐린다. [train_car.py 73–81행](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)
- **운영 준비 — 미확인** 입력 디렉터리와 출력 파일이 상대 경로로 고정된 일회성 학습 스크립트다. 서비스 운영 준비도는 적용 대상이 아니다. [train_car.py 63–83행](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)
- **유지보수 — 보완 필요** 데이터 위치·epoch·모델 크기가 코드 안에 있어 다른 데이터셋을 재현하려면 원본 스크립트를 편집해야 한다. [train_car.py 19–22·55–77행](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)

**좋은 점:** 실험의 전처리와 모델 구성이 한 파일에 드러난다. **개선 우선순위:** P2 — 그래프 x축을 실제 학습 기록 길이에서 만들고 데이터·하이퍼파라미터를 입력값으로 분리해 결과 해석 오류를 줄인다.

## 저장소 범위

이 저장소의 공개 파일은 `train_car.py` 한 개다. README나 학습 데이터·의존성 잠금 파일은 없다. 따라서 파일 이름 이상의 제품 목적이나 데이터 출처를 추정하지 않는다.
[원본: `train_car.py`](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)

## 스크립트가 하는 일

코드는 다섯 Conv2D·MaxPool·Dropout 묶음 뒤 Flatten·Dense와 3분류 softmax를 만든다. `ImageDataGenerator`가 `./input/data/train_data`와 `test_data` 폴더에서 128×128 이미지를 읽고 학습·검증에 공급한다. 완료되면 모델 파일과 JSON을 저장하고 정확도 그래프를 그리려 한다.
[원본: `train_car.py`](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)

## 정적 검토에서 보이는 제약

파일에는 60 epoch 학습 뒤 그래프용 epoch 열을 30개만 만드는 부분이 있다. 데이터 폴더와 런타임 버전이 없으므로 실행 성공이나 결과 정확도는 확인할 수 없다. 모델·그래프 출력 경로의 사용 가능 여부도 실행하지 않았다.
[원본: `train_car.py`](https://github.com/kdkrkwhr/dl-data-training/blob/a6b6af0142a3d57ebeac89c38c89d9dadd614c59/train_car.py)

## 연결해서 읽기

[차량 추적 자료](dl-object-tracking.md)의 TFRecord 변환과 목적·입력 형식이 다르다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
