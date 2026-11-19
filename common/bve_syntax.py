"""BVE 구문(.freeobj) 생성 공통 함수"""

TRACK_MODES = ('single', 'double')


def validate_track_mode(track_mode):
    if track_mode not in TRACK_MODES:
        raise ValueError(f'TRACK_MODE_INVALID: {track_mode!r}')


def rotation_for(direction: int) -> int:
    """선로 좌측(-1)이면 0도, 우측(1)이면 180도"""
    return 0 if direction == -1 else 180


def freeobj_line(station, track_idx, object_idx, x, y, rotation, comment=None) -> str:
    """``{sta},.freeobj {track};{idx};{x};{y};{rot};`` 한 줄 생성 (comment가 있으면 ``,;comment`` 추가)"""
    line = f"{station},.freeobj {track_idx};{object_idx};{x};{y};{rotation};"
    if comment is not None:
        line += f",;{comment}"
    return line + "\n"


def object_folder_from(target_directory: str) -> str:
    """대상 폴더 경로에서 BVE Object 폴더 기준 상대경로를 얻는다."""
    return target_directory.split("Object/")[-1]
