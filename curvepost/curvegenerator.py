import os

from common.base_generator import BaseObjectGenerator
from config import CURVE_PATHS
from curvepost.curve_output_manager import CURVEOutputManager
from curvepost.curve_processor import CurveProcessor
from curvepost.preprocessor import CurvePreprocessor
from infrastructure.filemanager import FileSystemService


class CurveGenerator(BaseObjectGenerator):
    """곡선표 제너레이터"""
    NAME = '곡선표'
    PATHS = CURVE_PATHS

    def build(self):
        info_path = self.state.info_path
        # 전략 선택
        builder = CurvePreprocessor.get_builder(info_path)

        # 전처리 + ip데이터빌드
        prepared = builder.preprocess(info_path, self.brokenchain)
        ipdatas = builder.build(prepared, self.brokenchain)

        # object데이터 빌드
        processor = CurveProcessor(self.source_directory, self.work_directory,
                                   self.state.target_directory, self.state.alignment_type, self.state.offset,
                                   self.state.start_index, self.log)
        return processor.build(self.start_sta, self.end_sta, ipdatas, self.structure_processor)

    def output_files(self, objectdatas):
        output_manager = self.create_output_manager(CURVEOutputManager)

        self.log("파일 저장 중...")
        post_file = os.path.join(self.work_directory, 'curve_post.txt')
        index_file = os.path.join(self.work_directory, 'curve_index.txt')
        FileSystemService.create_txt(post_file, output_manager.create_curve_post_txt(objectdatas))
        output_manager.create_curve_index_txt(objectdatas, index_file)

        self.copy_results(output_manager)
