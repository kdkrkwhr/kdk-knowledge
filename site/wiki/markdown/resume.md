---
{"id":"resume","type":"resource","order":76,"mapTitle":"공개 이력서 페이지의 구현","summary":"HTML·CSS로 구성된 정적 이력서 사이트의 게시 구조","sources":["resume-1","resume-2","resume-3"],"relations":[]}
---
# 공개 이력서 페이지의 구현

**분석 기준:** `31ca11c24755494362212f4bdc9c5718d49bfc64`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `31ca11c24755494362212f4bdc9c5718d49bfc64`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 별도 서버 없이 HTML·CSS로 게시하며 본문 구역을 소개·경력·프로젝트 등으로 나눴다. [index.html 24–85행](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/index.html)
- **구현 품질 — 양호** 스타일 파일을 상대 경로로 불러와 프로젝트 경로가 달라도 기본 문서 구조를 유지할 수 있다. [index.html 1–12행](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/index.html)
- **운영 준비 — 미확인** 정적 이력서여서 서버 장애 대응은 적용 대상이 아니다. 현재 공개 내용의 정확성·게시 상태는 별도 확인이 필요하고, 이 평가는 개인 경력의 진위를 판단하지 않는다. [README.md 1–30행](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/README.md)
- **유지보수 — 보완 필요** 스타일 정의가 압축된 긴 한 줄에 모여 있어 특정 규칙을 검토·수정하기 어렵다. [style.css 3행](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/style.css)

**좋은 점:** 정적 배포와 상대 경로라는 단순한 구성이 목적에 맞다. **개선 우선순위:** P3 — CSS 편집 원본을 읽기 쉬운 줄 단위로 유지하면 화면 변경 시 의도하지 않은 스타일 영향을 찾기 쉽다. 공개 내용의 갱신 승인은 별개다.

## 정적 페이지

README는 별도 빌드 없이 GitHub Pages에서 서비스하는 정적 이력서라고 설명한다. 루트 `index.html`이 내용을 담고 `style.css`를 상대 경로로 불러와 project Pages와 사용자 Pages 경로 모두를 고려한다. 실행 파일이나 데이터 서버는 없다.
[원본: `README.md`](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/README.md) [원본: `index.html`](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/index.html) [원본: `style.css`](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/style.css)

## 게시와 개인정보 경계

README는 공개 직책·기간·링크의 사전 확인과 회사 저장소 전체를 복사하지 말라는 주의를 명시한다. 여기서는 이력의 세부 문장, 이름 외 연락처, 성과 수치를 옮기지 않았다. 공개된 이력서가 곧 다른 자료의 재공개 승인이라고 해석하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/resume/blob/31ca11c24755494362212f4bdc9c5718d49bfc64/README.md)

## 연결해서 읽기

[Flutter 프로필 예제](flutter-profile.md)는 별도 UI 코드이고 [기술 블로그](kdkrkwhr.github.com.md)는 작성 글의 보관소다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
