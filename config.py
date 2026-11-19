"""프로그램 전역 설정값.

하드코딩되어 각 제너레이터에 흩어져 있던 작업 경로를 한 곳에 모은다.
경로를 바꾸려면 이 파일만 수정하면 된다.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratorPaths:
    """제너레이터별 작업 경로

    Attributes:
        source_root: 노선 종류별 소스 폴더들의 상위 폴더 (예: <source_root>/일반철도)
        work_directory: 중간 결과물을 만드는 작업 폴더
    """
    source_root: str
    work_directory: str


KM_PATHS = GeneratorPaths('c:/temp/km_post/소스/', 'c:/temp/km_post/result/')
CURVE_PATHS = GeneratorPaths('c:/temp/curve/소스/', 'c:/temp/curve/result/')
GRADE_PATHS = GeneratorPaths('c:/temp/pitch/소스/', 'c:/temp/pitch/result/')

# 선택 가능한 옵션
ALIGNMENT_TYPES = ['도시철도', '일반철도', '준고속철도', '고속철도']
POST_TYPES = ['거리표', '곡선표', '기울기표', '구조물표']
