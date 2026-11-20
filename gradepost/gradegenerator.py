import os

from common.base_generator import BaseObjectGenerator
from config import GRADE_PATHS
from gradepost.grade_output_manager import GradeOutputManager
from gradepost.preprocessor import VIPPreprocessor
from gradepost.profile_processor import ProfileProcessor
from infrastructure.filemanager import FileSystemService


class GradeGenerator(BaseObjectGenerator):
    """기울기표 제너레이터"""
    NAME = '기울기표'
    PATHS = GRADE_PATHS

    def build(self):
        info_path = self.state.info_path
        # 전략 선택
        builder = VIPPreprocessor.get_builder(info_path)

        # 전처리 + vip데이터빌드
        prepared = builder.preprocess(info_path, self.brokenchain)
        vipdatas = builder.build(prepared, self.brokenchain)

        # object데이터 빌드
        processor = ProfileProcessor(self.source_directory, self.work_directory,
                                     self.state.target_directory, self.state.alignment_type, self.state.offset,
                                     self.state.start_index, self.log)
        return processor.build(self.start_sta, self.end_sta, vipdatas, self.structure_processor)

    def output_files(self, objectdatas):
        output_manager = self.create_output_manager(GradeOutputManager)

        self.log("파일 저장 중...")
        post_file = os.path.join(self.work_directory, 'pitch_post.txt')
        index_file = os.path.join(self.work_directory, 'pitch_index.txt')
        FileSystemService.create_txt(post_file, output_manager.create_pitch_post_txt(objectdatas))
        output_manager.create_pitch_index_txt(objectdatas, index_file)

        self.copy_results(output_manager)
