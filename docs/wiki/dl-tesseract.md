---
{"id":"dl-tesseract","type":"project","order":73,"mapTitle":"Tesseract 번호판 OCR 실험","summary":"OpenCV 전처리·윤곽선 필터와 Tesseract 문자 인식 데모","sources":["dl-tesseract-1","dl-tesseract-2"],"relations":[]}
---
# Tesseract 번호판 OCR 실험

**분석 기준:** `d61bd752deb16ef19df40f420a038d81a21519ca`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

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
