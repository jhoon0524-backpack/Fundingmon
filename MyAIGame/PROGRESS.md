# 현재 진행 상황 (Handover Log)

## 최근 완료한 작업
- 프로젝트 초기 세팅 완료
- GAME_SPEC.md 기획서 작성 완료
- 기획서를 바탕으로 TASKS.md 작업 목록 60개 생성 완료
- [기반] 프로젝트 설정 파일을 텍스트로 작성 (project.godot, .gitignore, 폴더 구조, Main.tscn)
- [몬스터/시스템] 전투 규칙 코어 작성
  - `scripts/battle_rules.gd` — 속성 상성표, 데미지 계산, 영입 성공률
  - `scripts/idi_data.gd`, `scripts/move_data.gd` — 리소스 정의
  - `data/idis/` 아이디 3종, `data/moves/` 기술 4종
- [기획] 아이디 도감 12종으로 확장 (`IDI_DEX.md`)
  - 4속성 × 3단계 진화 계열, 기술 8종
  - 동급 대결 36개 조합이 모두 2~7턴에 끝나도록 스탯 검증
- [설계] 전투 상태 머신 설계 (`BATTLE_FLOW.md`)
  - 상태 9개, 행동 우선순위, 종료 조건 5가지 정리
  - TASKS.md 의 턴제 전투 항목을 5개에서 10개로 잘게 쪼갬
- [아트] 화풍 규격 문서 작성 (`ART_SPEC.md`)
  - 캔버스 크기, 23색 팔레트, 그리기 규칙, 애니메이션 프레임 수 고정
  - 필요 에셋 86장으로 산정. TASKS.md 에 [아트] 단계 추가
  - SpriteCook 을 생성 도구로 고정. 프롬프트 템플릿을 규격에 넣음
  - `tools/check_sprite.py` 작성 — 팔레트 이탈·반투명 픽셀·캔버스 크기 자동 검사
- [지침] `CLAUDE.md` 를 마스터 지침서 구조로 개편
  - 자율 루프 4대 원칙, 하이브리드 에셋 표준, QA 3단계, 종료 프로토콜
  - TASKS.md 에 파이썬 렌더링 3개와 [QA] 카테고리 4개 추가 (총 80개)

- [검증] 사용자 PC 에서 Godot 4.7.2 로 프로젝트를 열어 확인 (2026-09-12)
  - 에디터 정상 실행, 인풋 맵 6개, 해상도 640x360 / 창 1280x720, stretch viewport/keep,
    Nearest 필터, gl_compatibility 모두 적용 확인
  - `.tres` 20개(아이디 12, 기술 8) 에러 없이 로드, 진화 참조 8개 연결 확인
  - `--headless --quit-after 300` 에러 없이 종료
  - 전투 계산식 콘솔 검증 통과 (상성 4x4, 데미지, 영입 성공률)
  - 검증 스크립트 추가: `tools/verify_resources.gd`, `tools/verify_battle_rules.gd`
  - TASKS.md [기반] 9개, 데이터 정의 6개, QA 1개 체크 (총 16개)

- [데이터] 아이디 12종 `moves` 배열에 기술 연결 (2026-09-12)
  - 도감 표 그대로 1단계는 1단계 기술, 2·3단계는 2~3단계 기술 1개씩. 밸런스 검증 범위를 지키려고
    2·3단계에 1단계 기술을 같이 넣지 않았다. 기술을 늘릴 때는 36개 조합 턴 수를 다시 확인할 것
  - `.tres` 에 손으로 적은 타입 배열 문법 `Array[ExtResource("스크립트")]([...])` 이 정상 로드됨을 확인
- [플레이어] 임시 스프라이트 + Player 씬 + 4방향 이동 + 카메라 (2026-09-12)
  - `tools/render_player.py` 로 32x32 8장 렌더링 (4방향 x 2프레임). `check_sprite.py` 8장 모두 통과
  - `assets/sprites/player/player_frames.tres` SpriteFrames 4개 애니메이션, 8fps (2프레임 0.25초 루프)
  - `scenes/Player.tscn`: CharacterBody2D(원점=발밑) + AnimatedSprite2D + 발밑 12x8 충돌 + Camera2D
  - `scripts/player.gd`: 120px/s, 대각선 입력은 큰 축만 남기는 4방향 이동, 멈추면 첫 프레임 고정
  - `scenes/Main.tscn`: Player 를 (320,180) 에 배치, Camera2D 는 Player 자식으로 옮김
  - QA 1 통과, QA 2 는 `tools/qa_screenshot.gd` 가 오른쪽 입력을 30프레임 넣어 58px 이동 확인,
    QA 3 스크린샷에서 화면 중앙에 오른쪽 보는 플레이어 확인

## 다음에 진행할 작업
- [플레이어] TileMapLayer로 임시 필드 맵 1개 제작 (타일셋 1장이 먼저 필요 → [아트] 필드 타일셋 항목을 먼저 할 것)
- [플레이어] 맵 경계와 장애물에 충돌 타일 설정, 통과 불가 확인

## 버그 및 주의사항
- 이 PC 의 Godot 경로: `C:/Users/82103/Downloads/Godot_v4.7.2-stable_win64.exe/`
  (헤드리스 검증은 `_console.exe` 를 쓴다). PATH 에는 없다.
- 스크린샷 QA 명령 (창이 잠깐 뜬다. 헤드리스로는 렌더링이 안 되니 `--headless` 를 빼야 한다):
  `godot --path . --script tools/qa_screenshot.gd -- <저장할 png 절대경로>`
  메인 씬을 띄우고 오른쪽 입력을 30프레임 넣은 뒤 40프레임째에 640x360 으로 캡처한다.
  캡처 후 이미지 파일을 직접 읽어 확인할 것. 이 PC 는 오디오 장치가 없어 WASAPI 오류가
  찍히지만 더미 드라이버로 넘어가므로 무시해도 된다.
- 헤드리스 검증 명령 (에디터 없이 돌릴 수 있다):
  - `godot --headless --path . --script tools/verify_resources.gd` — 리소스·설정·인풋맵
  - `godot --headless --path . --script tools/verify_battle_rules.gd` — 전투 계산식
  - `godot --headless --path . --quit-after 300` — 메인 씬 실행 검사
- 에디터를 처음 열면 `project.godot` 을 Godot 이 자기 포맷으로 다시 쓴다
  (`config/features` 추가, 기본값인 `stretch/aspect="keep"` 은 생략, 인풋 이벤트 풀 포맷).
  값은 그대로이므로 놀라지 말 것. `.uid` 파일도 생성되는데 이건 커밋 대상이다.
- **아이디의 `moves` 배열은 비어 있다.** 타입 배열을 .tres 에 손으로 적으면
  깨질 위험이 있어 비워 뒀다. 에디터에서 각 아이디에 기술을 끌어다 넣을 것.
  어떤 기술을 넣을지는 `IDI_DEX.md` 의 기술 표 '사용 단계' 열을 볼 것.
- `evolves_into` 는 연결해 뒀다. 1단계 → 2단계 → 3단계 참조가 걸려 있다.
- 전투 계산식은 파이썬으로 옮겨 검증했다. 아이디 3종 기준 2~7턴에 전투가 끝난다.
- 스프라이트를 만들거나 채택하기 전 `ART_SPEC.md` 를 먼저 읽을 것.
  특히 8번 검수 항목을 통과하지 못한 에셋은 넣지 않는다.
- 스프라이트를 새로 만들면 반드시 `python3 tools/check_sprite.py <파일> --fix` 를 돌린다.
  AI 생성기는 팔레트를 정확히 지키지 못한다.
- `tools/check_sprite.py` 는 Pillow 가 필요하다. `pip install Pillow`
- SpriteCook MCP 서버는 아직 연결하지 않았다. 사용자 PC 에서 설정해야 한다.
- 커밋 포맷은 `feat: [TASKS 항목명] - 구현 내용` 이다. 이번 커밋부터 적용한다.
- QA 1 의 `--quit-after` 는 프레임 수다. 60 이면 약 1초라 씬이 뜨기 전에 끝난다.
  300 으로 적어 뒀으나 실제 값은 에디터에서 확인해 조정할 것.
- 전투 구현은 `BATTLE_FLOW.md` 를 먼저 읽고 시작할 것.
  구현 중 규칙이 바뀌면 그 문서부터 고친다.
- 스프라이트, 효과음 등 바이너리 에셋은 원격 작업 환경에서 만들 수 없다.
- 컴퓨터 없이 할 수 있는 작업은 여기까지다. 남은 항목은 모두
  에디터 작업(씬 편집, 타일맵)이나 바이너리 에셋이 필요하다.
