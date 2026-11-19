import os
from enum import Enum


class InfoFormat(Enum):
    """선형 정보 파일 형식"""
    BVE = 'BVE'          # .txt (BVE 구문에서 추출한 측점,값 목록)
    CIVIL3D = 'CIVIL3D'  # .xlsx (Civil3D 보고서)


_EXTENSION_MAP = {
    '.txt': InfoFormat.BVE,
    '.xlsx': InfoFormat.CIVIL3D,
}


def detect_info_format(path: str) -> InfoFormat:
    """파일 확장자로 정보 파일 형식을 판별한다."""
    ext = os.path.splitext(path)[1].lower()
    try:
        return _EXTENSION_MAP[ext]
    except KeyError:
        raise ValueError(f"지원하지 않는 정보 파일 형식: '{ext}' ({path})") from None
