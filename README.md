# OpenBVEPostCreator
OPENBVE용 선로제표 자동생성 및 편집도구 개발 프로젝트


BVE 선로제표(거리표·곡선표·기울기표) 오브젝트/구문 생성기.

## 구조

```
main.py                 진입점 (Tk GUI)
config.py               작업 경로·옵션 목록 (c:/temp/... 경로는 여기서만 관리)
controller/             AppController, AppState, 사전설정(PreRunSetup), MainRunner
common/
  base_generator.py     제너레이터 공통 템플릿: 디렉토리 준비 → 측점 계산 → 구조물 로드 → build → output_files
  generator_factory.py  제표 종류 → 제너레이터 매핑
  output_manager.py     .freeobj 구문/인덱스 파일 생성 + 결과 복사 공통 클래스
  bve_syntax.py         .freeobj 한 줄 생성, 회전/트랙모드 검증 등 BVE 구문 헬퍼
  info_format.py        정보 파일(.txt=BVE / .xlsx=Civil3D) 판별
kmpost/ curvepost/ gradepost/   제표별 빌더·프로세서·출력 매니저
infrastructure/         파일/CSV/DXF→이미지/구조물 엑셀 처리
gui/                    Tk 위젯 및 대화상자
tests/                  pytest
```

새 제표 종류를 추가하려면 `BaseObjectGenerator`를 상속해 `NAME`, `PATHS`, `build()`, `output_files()`만 구현하고
`GeneratorFactory.GENERATORS` 와 `config.POST_TYPES` 에 등록한다.

## 테스트

```
pip install ezdxf pymupdf pandas openpyxl pillow matplotlib numpy pytest
python -m pytest tests
```
