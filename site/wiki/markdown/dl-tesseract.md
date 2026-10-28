---
{"id":"dl-tesseract","type":"project","order":73,"mapTitle":"Tesseract 번호판 OCR 실험","summary":"OpenCV 전처리·윤곽선 필터와 Tesseract 문자 인식 데모","sources":["dl-tesseract-1","dl-tesseract-2"],"relations":[]}
---
# Tesseract 번호판 OCR 실험

**분석 기준:** `d61bd752deb16ef19df40f420a038d81a21519ca`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `d61bd752deb16ef19df40f420a038d81a21519ca`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 흐림·이진화·윤곽 검출·문자 인식의 실험 단계를 함수로 나눴다. [main.py 9–43·93–125행](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)
- **구현 품질 — 보완 필요** 이미지 읽기 결과가 없는 경우를 확인하기 전에 전처리를 시작한다. 입력 파일이 없거나 읽을 수 없으면 실패 원인이 흐려진다. [main.py 120–125행](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)
- **운영 준비 — 미확인** 한 장의 고정된 로컬 이미지를 GUI로 보여 주는 실험이며 배치·서비스 운영 대상으로 작성된 증거는 없다. [main.py 117–126행](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)
- **유지보수 — 보완 필요** 윤곽 함수의 반환값 세 개를 고정으로 받으므로 OpenCV API 형태에 결합돼 있다. 의존성 버전과 입력 예제를 기록하면 재현성이 좋아진다. [main.py 20–24·37–44행](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)

**좋은 점:** 전처리와 인식의 단계가 명시적이다. **개선 우선순위:** P2 — 입력 파일 확인과 윤곽 반환형 처리 경계를 두면 환경·입력 차이에서 원인을 빠르게 알 수 있다.

## 이미지 처리 흐름

`main.py`는 고정된 테스트 이미지를 읽고 GaussianBlur, 회색 변환, Canny·임계값, morphology로 후보 윤곽선을 만든다. 사각형의 회전·면적·종횡비를 검사한 뒤 후보 영역을 잘라 Tesseract로 문자를 읽고 화면에 덧쓴다.
[원본: `main.py`](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)

README는 OpenCV·Tesseract 버전과 샘플 이미지를 안내한다. 테스트 이미지 폴더가 있지만 이 정적 분석에서 OCR 결과나 인식률을 재현하지 않았다.
[원본: `README.md`](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/README.md) [원본: `main.py`](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py)

## 호환성 경계

코드는 `cv2.findContours`의 반환값 세 개를 받는 형태라 OpenCV 버전에 민감하다. README의 환경을 벗어난 최신 설치에서 동일하게 동작한다고 보장하지 않는다.
[원본: `main.py`](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/main.py) [원본: `README.md`](https://github.com/kdkrkwhr/dl-tesseract/blob/d61bd752deb16ef19df40f420a038d81a21519ca/README.md)

## 연결해서 읽기

[YOLO 객체 검출](dl-object-detecting.md)과는 이미지 처리 목표가 다르다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
