# kdk-knowledge

김동기의 프로젝트, 경력과 역할, 기술 선택과 배움, 경험에서 나온 개발 기준을 **공개 근거와 연결**하기 위한 개인 지식 허브입니다. 개발 기준은 한 영역입니다. 아직 근거가 등록되지 않은 경력·성과·기술 선택은 공개 위키에 빈 상태로 남깁니다.

- [프로젝트 중심 위키](https://kdkrkwhr.github.io/kdk-knowledge/)
- [근거 관계 지도](https://kdkrkwhr.github.io/kdk-knowledge/architecture/)
- [입력 템플릿](templates/README.md)

## 현재 범위

첫 사례는 공개 [Notebook Pets](https://github.com/kdkrkwhr/notebook-pets/tree/ca5648b49e6d0a67526856a930090173d0454389)와 [Auction Spot API](https://github.com/kdkrkwhr/auction-spot-api/tree/7c2d9496a5ae0f1dcd0345196483c2674ecff140)의 README·코드를 읽어 만들었습니다. 다른 저장소에 위키가 있어야 연결되는 구조가 아닙니다. 원본 저장소는 수정하거나 자동 동기화하지 않습니다. [Engineering Standards](https://github.com/kdkrkwhr/engineering-standards/tree/e1c019df54898e928f871602b76fa463d3ec7930)는 참고할 개발 기준으로 별도 기록했으며, 사례 프로젝트에 실제 적용됐다고 표시하지 않습니다. `site/knowledge.json`의 출처 URL과 커밋은 검토한 버전으로 고정했습니다. 새 커밋을 반영하려면 차이를 읽고 해설과 출처를 함께 갱신합니다.

공개 저장소 목록은 살폈지만 전체 프로젝트·이력 수집을 마친 상태는 아닙니다. 첫 사례는 서로 다른 실행 환경과 언어가 드러나고, README와 구체적 코드 파일을 함께 대조할 수 있는 두 프로젝트로 제한했습니다.

`site/index.html`은 프로젝트별 질문, 공개 코드에서 확인한 구현, 아직 모르는 선택 이유·배움을 구분하는 해설입니다. `site/architecture/`는 JSON에 사람이 등록한 프로젝트·기술·구현 관계를 탐색합니다. **Graphify는 이 저장소에서 설치하거나 실행하지 않았습니다.** 이 허브에서 자동 추출을 시작할 때는 공식 소스와 버전, 실행 환경, 공개 입력 범위, 외부 전송 여부를 먼저 결정해야 합니다. 자동 추출 관계와 해설·편집 관계에는 각각 다른 출처와 기준 커밋을 붙입니다.

## 추가와 검증

1. 공개 저장소 목록에서 원본 README·코드·문서를 고릅니다. 위키 유무는 수집 조건이 아닙니다. [템플릿](templates/README.md)에 공개 가능한 프로젝트·경력·기술·결정·학습 사실과 근거를 정리합니다. 비공개 초안은 이 공개 저장소에 저장하지 않습니다.
2. `site/knowledge.json`에 출처, 항목, 관계를 추가합니다. 관계마다 출처 ID를 붙이고 고정 커밋의 원본 URL을 사용합니다.
3. `site/index.html`의 해설을 소스와 사람이 다시 대조합니다. 근거 변경만으로 해설이 자동 수정되지는 않습니다.
4. `python3 scripts/validate.py`와 `python3 -m unittest discover -s tests -v`를 실행합니다. 정적 파일은 `python3 -m http.server 8000 -d site`로 미리 볼 수 있습니다.
5. GitHub Actions가 공개 산출물 `site/`만 검사 후 Pages에 업로드합니다. 실제 공개 여부는 Actions와 URL 응답을 별도로 확인합니다.

외부 LLM 호출, 유료 API, 실시간 챗봇, Graphify 실행은 현재 흐름에 없습니다.
