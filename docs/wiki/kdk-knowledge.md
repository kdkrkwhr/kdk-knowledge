---
{"id":"kdk-knowledge","type":"project","order":78,"mapTitle":"중앙 지식 허브 구현","summary":"공개 원본 커밋을 Markdown 문서·검색·관계 지도로 빌드하는 저장소","sources":["kdk-knowledge-1","kdk-knowledge-2","kdk-knowledge-3"],"relations":[{"to":"standards","label":"개발 기준을 한 참고 자료로 문서화","evidence":["kdk-knowledge-1"]}]}
---
# 중앙 지식 허브 구현

**분석 기준:** `518ccf03c2b798b64e628eb7e3332561345155ef`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 편집 원본과 생성물

README는 `docs/wiki/*.md`를 사람이 읽고 수정하는 원본으로 지정한다. `scripts/build_wiki.py`가 front matter와 본문을 읽어 정적 HTML·Markdown 원본 복사·검색 인덱스·관계 JSON을 생성한다. 현재 문서와 지도는 원본 저장소의 동작에 대한 사람이 쓴 설명이며 원본 저장소를 자동 변경하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/README.md) [원본: `scripts/build_wiki.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/scripts/build_wiki.py)

## 검증 경계

`scripts/validate.py`는 등록된 근거 URL의 저장소·커밋·경로 일치, 공개 여부, 문서 링크와 관계 근거를 검사한다. 이 검사는 원본 코드 실행이나 진술의 의미적 진실 전체를 자동 판정하지 않는다. 관계는 편집 데이터이며 Graphify 추출은 아직 수행하지 않았다.
[원본: `scripts/validate.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/scripts/validate.py) [원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/README.md)

## 버전 기준

이 문서는 허브 자체의 첫 공개 Markdown 빌드 시점인 고정 커밋을 근거로 한다. 이후 문서가 늘어나더라도 기존 커밋의 구현 설명과 현재 사이트 산출물은 별도 시점일 수 있다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/README.md) [원본: `scripts/build_wiki.py`](https://github.com/kdkrkwhr/kdk-knowledge/blob/518ccf03c2b798b64e628eb7e3332561345155ef/scripts/build_wiki.py)

## 연결해서 읽기

[문서 갱신 절차](maintenance.md)가 새로운 근거를 등록하는 방법을, [공개 저장소 목록](repositories.md)이 범위를 설명한다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
