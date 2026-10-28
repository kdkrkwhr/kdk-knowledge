---
{"id":"kdkrkwhr.github.com","type":"resource","order":75,"mapTitle":"개인 기술 블로그 저장소","summary":"Jekyll 게시 구조와 Markdown 글·발행 확인 스크립트","sources":["kdkrkwhr.github.com-1","kdkrkwhr.github.com-2","kdkrkwhr.github.com-3","kdkrkwhr.github.com-4"],"relations":[{"to":"agent-hub","label":"블로그 프로젝트 목록이 agent-hub를 연결","evidence":["kdkrkwhr.github.com-3"]}]}
---
# 개인 기술 블로그 저장소

**분석 기준:** `02bb498ac183973e58e6b6489f59971e63691ac3`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `02bb498ac183973e58e6b6489f59971e63691ac3`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** Jekyll 설정, 게시 글, 프로젝트 데이터가 분리돼 공개 콘텐츠의 위치를 찾기 쉽다. [README.md 1–22행](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/README.md) [projects.yml 1–18행](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_data/projects.yml)
- **구현 품질 — 보완 필요** 게시 확인 스크립트는 URL·예상 문구를 확인하지만 실패 시에도 종료 코드 0을 사용한다. 이를 실패 차단 단계로 연결하면 오류가 성공처럼 전달될 수 있다. [publish_blog.py 26–54행](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/scripts/publish_blog.py)
- **운영 준비 — 미확인** 설정에 Pages 주소가 있고 게시 확인 경로도 있지만 현재 공개 상태·운영 책임은 고정 파일만으로 판단하지 않는다. [config.yml 1–12행](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_config.yml)
- **유지보수 — 양호** 프로젝트 목록을 데이터 파일로 분리해 항목 링크를 한곳에서 고칠 수 있다. [projects.yml 1–18행](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_data/projects.yml)

**좋은 점:** 콘텐츠와 프로젝트 목록의 편집 위치가 구분돼 있다. **개선 우선순위:** P2 — 게시 확인 스크립트가 검증용으로 쓰일 때 실패 종료 코드를 반환하도록 모드를 분리해 배포 실패를 숨기지 않는다.

## 콘텐츠와 빌드 구조

README는 Jekyll·Kramdown을 쓰는 GitHub Pages 기술 블로그라고 설명한다. `_config.yml`은 사이트 설정을, `_posts`는 날짜가 붙은 Markdown 글을, `_data/projects.yml`은 프로젝트 목록 데이터를 담는다. 글에서 표현한 경험은 개인의 해석이 포함될 수 있으므로 이 문서에서는 출판 구조만 기술한다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/README.md) [원본: `_config.yml`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_config.yml) [원본: `_data/projects.yml`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_data/projects.yml)

## 게시 확인 경로

`scripts/publish_blog.py`는 한 글의 공개 URL을 최대 세 차례 조회하고 응답 내용에 예상 문자열이 있는지 확인해 로그를 남긴다. 실패해도 종료 코드는 0으로 반환하도록 작성돼 있으므로 이 스크립트가 CI 배포 성공을 엄격하게 보증한다고 설명하지 않는다.
[원본: `scripts/publish_blog.py`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/scripts/publish_blog.py)

## 공개 범위

원본 README와 데이터에는 개인 식별·연락 정보가 포함될 수 있다. 이 위키는 이메일·연락처·개별 경력 서술을 복제하지 않고 블로그 구조와 소스 경계만 연결한다.
[원본: `README.md`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/README.md) [원본: `_data/projects.yml`](https://github.com/kdkrkwhr/kdkrkwhr.github.com/blob/02bb498ac183973e58e6b6489f59971e63691ac3/_data/projects.yml)

## 연결해서 읽기

블로그에 소개된 [노트버디](notebuddy.md) 등의 기술 글은 프로젝트 코드 자체와 별개의 서술 근거다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
