from common.bve_syntax import freeobj_line, rotation_for, validate_track_mode
from infrastructure.filemanager import FileSystemService


class BaseOutputManager:
    """결과물(구문 텍스트, 인덱스 파일) 생성 및 대상 폴더 복사 공통 기능"""

    def __init__(self, work_directory, target_directory, offset, mode, direction, index):
        self.work_directory = work_directory
        self.target_directory = target_directory
        self.offset = offset
        self.track_mode = mode
        self.track_direction = direction
        self.track_index = index

    def copy_result_files(self, include_ext=None, exclude_ext=None):
        FileSystemService.copy_all_files(
            self.work_directory, self.target_directory,
            include_ext or ['.csv', '.png', '.txt', '.jpg'],
            exclude_ext or ['.dxf', '.ai']
        )

    def create_post_lines(self, data_list, prefix: str, type_attr: str) -> list[str]:
        """오브젝트 데이터 목록을 .freeobj 구문 목록으로 변환

        Args:
            data_list: no, structure, station, object_index, offset 속성을 가진 객체 목록
            prefix: 주석 접두어 (예: 'IP', 'VIP')
            type_attr: 주석에 넣을 종류 속성명 (예: 'curvetype', 'vcurve_type')
        """
        validate_track_mode(self.track_mode)
        texts = []
        for data in data_list:
            kind = getattr(data, type_attr)
            if self.track_mode == 'single':
                texts.append(self._line(data, 'main', f"{prefix}{data.no}_{kind}-{data.structure}"))
            else:
                texts.append(self._line(data, 'main', f"{prefix}{data.no}하_{kind}-{data.structure}"))
                texts.append(self._line(data, 'sub', f"{prefix}{data.no}상_{kind}-{data.structure}"))
        return texts

    def _line(self, data, track: str, comment: str) -> str:
        direction = self.track_direction[track]
        x = direction * self.offset[data.structure][0]
        return freeobj_line(data.station, self.track_index[track], data.object_index,
                            x, data.offset[1], rotation_for(direction), comment)

    @staticmethod
    def write_index_txt(data_list, output_file):
        """.freeobj(idx) 경로 정의 파일 저장"""
        FileSystemService.create_txt(
            output_file,
            [f".freeobj({d.object_index}) {d.object_path}/{d.filename}.csv\n" for d in data_list]
        )
