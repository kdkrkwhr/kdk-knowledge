---
{"id":"kdkrkwhr.github.com","type":"project","order":75,"mapTitle":"개인 기술 블로그 저장소","summary":"Jekyll 게시 구조와 Markdown 글·발행 확인 스크립트","sources":["kdkrkwhr.github.com-1","kdkrkwhr.github.com-2","kdkrkwhr.github.com-3","kdkrkwhr.github.com-4"],"relations":[{"to":"agent-hub","label":"블로그 프로젝트 목록이 agent-hub를 연결","evidence":["kdkrkwhr.github.com-3"]}]}
---
# 개인 기술 블로그 저장소

**분석 기준:** `02bb498ac183973e58e6b6489f59971e63691ac3`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

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
