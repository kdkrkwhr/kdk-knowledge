---
{"id":"spring-ai","type":"reference","order":79,"mapTitle":"Spring AI fork 참조","summary":"upstream Spring AI 코드를 가리키는 fork; 독자 커밋 확인 안 됨","sources":["spring-ai-1","spring-ai-2"],"relations":[{"to":"spring-boot","label":"upstream README가 Spring Boot 호환성을 설명","evidence":["spring-ai-1"]}]}
---
# Spring AI fork 참조

**분석 기준:** `c988e72ab7282bcc352b2155e8cb27ff4b5e0fda`. 이 문서는 공개 원본 파일을 정적으로 읽어 작성했다. 해당 프로젝트의 설치·실행·테스트를 수행하거나 개인 담당 범위·성과를 확인한 것은 아니다.

## 출처와 구성

GitHub fork 메타데이터는 원본을 `spring-projects/spring-ai`로 표시한다. 고정 커밋의 README도 Spring 친화적 AI API와 모델·벡터 저장소·RAG 통합을 upstream 프로젝트의 목표로 설명한다. 루트 `pom.xml`은 BOM, 모델, 벡터 저장소, 자동 설정 등을 모듈로 나누는 Maven parent다. 이 기술 구현을 계정 소유자의 개인 성과로 서술하지 않는다.
[원본: `README.md`](https://github.com/kdkrkwhr/spring-ai/blob/c988e72ab7282bcc352b2155e8cb27ff4b5e0fda/README.md) [원본: `pom.xml`](https://github.com/kdkrkwhr/spring-ai/blob/c988e72ab7282bcc352b2155e8cb27ff4b5e0fda/pom.xml)

## 기여 확인 상태

2026-10-27 공개 GitHub compare 조회에서는 fork 기본 브랜치가 upstream `main`보다 뒤에 있고 앞선 커밋은 0개였다. 이는 **기본 브랜치 비교의 스냅샷**이며 다른 브랜치·외부 PR 기여 전체를 조사한 결과가 아니다. 개인이 Spring AI를 실제 프로젝트에 적용했다는 근거도 이 fork만으로는 없다.
[원본: `README.md`](https://github.com/kdkrkwhr/spring-ai/blob/c988e72ab7282bcc352b2155e8cb27ff4b5e0fda/README.md) [원본: `pom.xml`](https://github.com/kdkrkwhr/spring-ai/blob/c988e72ab7282bcc352b2155e8cb27ff4b5e0fda/pom.xml)

## 연결해서 읽기

[개발 기준](standards.md)이나 [Spring Boot 예제](spring-boot.md)와 기술 이름은 겹치지만 적용 관계는 별도 근거가 필요하다.

## 확인 범위와 미확인 사항

위 구현 설명은 표시한 커밋의 파일에서 확인한 사실과 정적 해석이다. 현재 배포·운영 상태, 실행 성공, 실제 사용량, 개인 선택 이유와 기여 범위는 확인하지 않았다.
