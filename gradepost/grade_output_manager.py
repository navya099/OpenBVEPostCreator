from common.output_manager import BaseOutputManager
from model.grade.vip_object_data import VIPObjectDATA


class GradeOutputManager(BaseOutputManager):
    """기울기표 출력 매니저"""

    def create_pitch_post_txt(self, data_list: list[VIPObjectDATA]) -> list[str]:
        return self.create_post_lines(data_list, prefix='VIP', type_attr='vcurve_type')

    @staticmethod
    def create_pitch_index_txt(data_list: list[VIPObjectDATA], output_file):
        BaseOutputManager.write_index_txt(data_list, output_file)
