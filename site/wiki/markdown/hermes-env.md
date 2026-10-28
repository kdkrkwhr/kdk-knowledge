---
{"id":"hermes-env","type":"project","order":26,"mapTitle":"Hermes 환경 템플릿","summary":"Hermes 작업 환경의 경로·프로필·스킬을 다른 머신에 배치하는 부트스트랩 저장소","sources":["env-readme","env-bootstrap","env-agent-guide","env-config","env-conventions"],"relations":[]}
---
# hermes-env: 작업 환경을 다시 구성하는 부트스트랩

이 저장소는 제품 코드나 개인 메모리의 복사본이 아니라 Hermes 작업 환경의 **디렉터리 구조, 프로필 설정 템플릿, 스킬, 운영 규칙**을 담는다. README는 프로젝트 코드·SSoT 본문·시크릿 값은 포함하지 않는다고 구분한다. 이 문서는 `bootstrap.sh`가 실제로 어떤 파일을 만들거나 보존하는지 읽었다. 스크립트는 실행하지 않았다. [저장소 설명](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/README.md) · [부트스트랩 코드](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)

## 냉정한 기술 평가

**평가일:** 2026-10-28 · **근거 커밋:** `ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39`. 공개 소스의 정적 평가이며 실제 운영 결과나 개인의 기여 범위를 확정하지 않는다.

- **구조·설계 — 양호** 입력 경로·선택 기능·확인 전용 모드를 구분하고 기존 설정과 시크릿 파일은 기본적으로 보존한다. [bootstrap.sh 17–47·128–185행](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)
- **구현 품질 — 보완 필요** 경로를 sed 치환식에 그대로 넣고 확인 모드에서 경로를 포함한 문자열을 eval로 실행한다. 구분자나 따옴표가 들어간 경로에서는 치환·검사가 깨질 수 있다. [bootstrap.sh의 subst·doctor, 69–115행](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)
- **운영 준비 — 미확인** 일반 실행은 Hermes 설치 스크립트를 호출하며 선택 옵션은 추가 설치·연동을 수행한다. 실제 Mac 환경에서의 완료 상태는 이 정적 평가로 확인하지 않는다. [bootstrap.sh 134–140·187–205행](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)
- **유지보수 — 양호** 단계별 출력과 완료/미완료 판정이 있어 구성 절차를 추적하기 쉽다. [bootstrap.sh의 doctor, 95–115·204–208행](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)

**좋은 점:** 선택 기능을 명시적 플래그로 제한하고 기존 파일 보존을 기본으로 삼았다. **개선 우선순위:** P2 — 경로 치환을 문자열 대체 API로 바꾸고 eval 없는 파일 검사를 사용하면 특수문자 경로에서도 예측 가능해진다.

## 입력과 배치 경계

스크립트는 프로젝트 코드 루트와 E2E 루트를 받고, Hermes 홈은 기본값을 둘 수 있다. 비대화형 환경에서 필수 경로가 없으면 실패한다. 정상 실행 경로에서는 디렉터리를 만들고, Hermes CLI가 없다면 설치 래퍼를 호출한다. 그 뒤 config 템플릿의 경로 플레이스홀더를 치환하고, 역할별 `pm/dev/infra/qa/ops` 설정을 배치한다. `--ssot-url`이 지정되고 대상 폴더가 비어 있을 때만 별도 SSoT를 clone한다. [옵션·단계 구현](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh) · [에이전트용 절차](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/AGENT_BOOTSTRAP.md)

기존 `config.yaml`, 역할 config, `.env.local`은 건너뛰도록 구현돼 있다. 반면 `--with-souls`는 SOUL 파일 덮어쓰기를 명시적으로 선택하고, 스킬 복사는 `cp -r`로 진행한다. 따라서 README의 멱등 설명을 **모든 파일이 변경되지 않는다는 뜻**으로 확대하지 않는다. `--with-coral`은 선택적 설치·셋업 경로이며 기본 실행과 구분한다. [파일 복사 조건](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh)

## 검증 모드와 설정의 역할

`--check`는 설치·복사 단계 전에 `doctor`를 실행하고, 지정 디렉터리, CLI, config, 스킬, `.env.local`, 역할별 config의 존재를 확인한다. 실제 기능 통합 테스트가 아니라 로컬 파일 상태 점검이다. `hermes/config.yaml.template`는 모델·프로바이더·API 키 값 대신 워크플로 설정과 경로 힌트를 제공한다. [검증 구현](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/bootstrap.sh) · [설정 템플릿](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/hermes/config.yaml.template)

[컨벤션 문서](https://github.com/kdkrkwhr/hermes-env/blob/ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39/docs/conventions.md)는 코드 저장소, SSoT, 보고서, 시크릿 파일의 위치를 구분한다. 이것은 다른 도구가 자동으로 강제하는 보안 경계가 아니라, 부트스트랩과 사용자가 유지해야 할 운영 규칙이다. [AGENT HUB](agent-hub.md)처럼 CLI 작업을 수행하는 도구와 달리, 이 저장소의 중심 기능은 환경을 구성하는 과정이다.

## 확인 범위와 미확인 사항

검토한 판은 `ecf8b93ec6e7003bfd640f67b3cb90e25ad61b39`다. 머신에서 부트스트랩·Hermes CLI 설치·Coral 연결을 실행하거나 확인하지 않았다. 개인이 이 구조를 택한 이유, 여러 머신에서의 재현 성공률, 실제 시크릿 관리 상태도 공개 파일만으로 확정할 수 없다. 원본의 경로 예시는 이 공개 위키에 재노출하지 않는다.
