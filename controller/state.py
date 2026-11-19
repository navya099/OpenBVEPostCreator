# controller/state.py
from dataclasses import dataclass


@dataclass
class AppState:
    """GUI와 제너레이터가 공유하는 실행 상태"""
    start_station: float = 0.0
    end_station: float = 0.0
    reverse_start: float = 0.0
    is_reverse: bool = False
    brokenchain: float = 0.0
    isbrokenchain: bool = False
    alignment_type: str = ''
    structure_excel_path: str = ''
    offset: dict | None = None          # {'토공': (x, y), '교량': (x, y), '터널': (x, y)}
    target_directory: str = ''
    posttype: str = ''
    track_distance: float = 0.0
    start_index: int = 0
    track_mode: str = ''                # 'single' | 'double'
    track_direction: dict | None = None  # {'main': -1|1, 'sub': -1|1|None}
    track_index: dict | None = None      # {'main': int, 'sub': int|None}
    info_path: str = ''

    @property
    def effective_brokenchain(self) -> float:
        """'파정 사용'이 체크된 경우에만 파정값을 적용한다."""
        return (self.brokenchain or 0.0) if self.isbrokenchain else 0.0
