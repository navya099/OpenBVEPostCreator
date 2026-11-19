from common.output_manager import BaseOutputManager
from model.curve.curve_object_data import CurveObjectDATA


class CURVEOutputManager(BaseOutputManager):
    """곡선표 출력 매니저"""

    def create_curve_post_txt(self, data_list: list[CurveObjectDATA]) -> list[str]:
        return self.create_post_lines(data_list, prefix='IP', type_attr='curvetype')

    @staticmethod
    def create_curve_index_txt(data_list: list[CurveObjectDATA], output_file):
        BaseOutputManager.write_index_txt(data_list, output_file)
