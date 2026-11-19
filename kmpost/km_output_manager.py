import os

from common.output_manager import BaseOutputManager
from infrastructure.csvmanager import CSVManager
from infrastructure.filemanager import FileSystemService
from kmpost.imgdatafactory import KMImageDataFactory
from kmpost.img_generator import KMImageGenerator
from kmpost.syntax_factory import KMBVESyntaxFactory


class KMOutputManager(BaseOutputManager):
    """KM 결과 파일, 이미지, CSV, BVE 구문 처리"""

    def save_txt_files(self, index_datas, post_datas):
        index_file = os.path.join(self.work_directory, 'km_index.txt')
        post_file = os.path.join(self.work_directory, 'km_post.txt')
        FileSystemService.create_txt(index_file, index_datas)
        FileSystemService.create_txt(post_file, post_datas)

    def generate_images_csv_bve(self, builder_results, source_directory, alignment_type, start_idx):
        """Builder에서 생성한 sta, post_type, structure 결과를 이용해 이미지/CSV/BVE 생성"""
        index_datas = []
        post_datas = []
        syntax_factory = KMBVESyntaxFactory(start_idx)
        for i, (stadata, post_type, structure) in enumerate(builder_results):
            imgdata = KMImageDataFactory.create(post_type, stadata.after_sta, structure)
            KMImageGenerator.generate(imgdata, post_type, alignment_type, source_directory, self.work_directory)
            CSVManager.copy_and_export_csv(
                imgdata.openfile_name, imgdata.imgname,
                source_directory=source_directory,
                work_directory=self.work_directory,
                replacements={f'LoadTexture, {post_type}.png,': f'LoadTexture, {imgdata.imgname}.png,'}
            )
            index, post = syntax_factory.create(
                i=i, station=stadata, structure=structure, target_directory=self.target_directory,
                track_index=self.track_index, offset=self.offset, track_mode=self.track_mode,
                track_direction=self.track_direction)
            index_datas.append(index)
            post_datas.append(post)
        return index_datas, post_datas
