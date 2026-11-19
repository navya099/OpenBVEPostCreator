from common.base_generator import BaseObjectGenerator
from config import KM_PATHS
from kmpost.kmbuilder import KMObjectBuilder
from kmpost.km_output_manager import KMOutputManager


class KMGenerator(BaseObjectGenerator):
    """거리표 제너레이터"""
    NAME = '거리표'
    PATHS = KM_PATHS

    def build(self):
        interval = 100 if self.state.alignment_type == '도시철도' else 200
        self.log("KM Object 생성 중...")
        builder = KMObjectBuilder(
            self.start_sta,
            self.end_sta,
            structure_processor=self.structure_processor,
            alignmenttype=self.state.alignment_type,
            offset=self.state.offset,
            interval=interval,
            reverse_start=self.state.reverse_start,
            is_reverse=self.state.is_reverse
        )
        return builder.run()

    def output_files(self, builder_results):
        output_manager = self.create_output_manager(KMOutputManager)
        index_datas, post_datas = output_manager.generate_images_csv_bve(
            builder_results, self.source_directory, self.state.alignment_type, self.state.start_index
        )
        self.log("파일 저장 중...")
        output_manager.save_txt_files(index_datas, post_datas)
        self.log("파일 복사 중...")
        output_manager.copy_result_files()
