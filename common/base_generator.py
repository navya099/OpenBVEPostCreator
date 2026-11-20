import os

from config import GeneratorPaths
from infrastructure.filemanager import FileSystemService
from infrastructure.structuresystem import StructureProcessor


class BaseObjectGenerator:
    """선로제표 제너레이터 공통 뼈대 (Template Method)

    하위 클래스는 ``NAME``, ``PATHS`` 를 지정하고 ``build`` / ``output_files`` 만 구현한다.
    """
    NAME: str = ''
    PATHS: GeneratorPaths | None = None

    def __init__(self, state, logger, paths: GeneratorPaths | None = None):
        self.state = state
        self.log = logger
        paths = paths or self.PATHS
        self.base_source_directory = paths.source_root if paths else ''
        self.work_directory = paths.work_directory if paths else ''
        self.source_directory = ''
        self.structure_processor = None
        self.start_sta = 0.0
        self.end_sta = 0.0

    @property
    def brokenchain(self) -> float:
        return self.state.effective_brokenchain

    # ── 템플릿 메서드 ─────────────────────────────────────────────
    def generate(self):
        try:
            self.log(f"{self.NAME} 생성 시작")
            self.prepare_directories()
            self.start_sta, self.end_sta = self.calculate_stations()
            self.load_structure_processor()
            results = self.build()
            self.output_files(results)
            self.log("모든 작업이 완료됐습니다.")
        except Exception as e:
            self.log(f"[오류] {e}")

    def build(self):
        raise NotImplementedError

    def output_files(self, results):
        raise NotImplementedError

    # ── 공통 단계 ─────────────────────────────────────────────────
    def calculate_stations(self):
        bc = self.brokenchain
        return self.state.start_station + bc, self.state.end_station + bc

    def prepare_directories(self):
        self.source_directory = os.path.join(self.base_source_directory, self.state.alignment_type)
        self.log(f"소스 경로: {self.source_directory}")

        # 작업 폴더는 프로그램 전용 임시 폴더이므로 매번 비우고 시작한다
        FileSystemService.reset_directory(self.work_directory)
        FileSystemService.copy_files(
            self.source_directory,
            self.work_directory,
            include_extensions=['.jpg', '.png'],
            exclude_extensions=['.dxf', '.ai', '.csv'],
        )
        self.log(f"작업 디렉토리: {self.work_directory}")
        self.log(f"대상 디렉토리: {self.state.target_directory}")

    def copy_results(self, output_manager):
        """결과물을 대상 폴더로 복사 (대상 폴더의 기존 파일은 유지, 같은 이름만 덮어씀)"""
        self.log("파일 복사 중...")
        copied, overwritten = output_manager.copy_result_files()
        self.log(f"파일 {copied}개 복사 완료 (기존 파일 덮어씀: {overwritten}개)")

    def load_structures(self):
        processor = StructureProcessor(self.state.structure_excel_path)
        processor.process_structure(self.brokenchain)
        return processor

    def load_structure_processor(self):
        self.log("구조물 정보 불러오는 중...")
        self.structure_processor = self.load_structures()
        self.log("구조물 정보가 성공적으로 로드되었습니다.")

    def create_output_manager(self, manager_cls):
        return manager_cls(
            self.work_directory,
            self.state.target_directory,
            self.state.offset,
            self.state.track_mode,
            self.state.track_direction,
            self.state.track_index
        )
