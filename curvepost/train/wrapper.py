from curvepost.curveline.output_service import CurveOutputService
from curvepost.spiral_processor import SpiralProcessor
from curvepost.train.output_manager import TrainOutputManager
from curvepost.train.post_data import TrainPostData
from curvepost.train.train_processor import TrainProcessor


class TrainLineProcessorWrapper:
    def __init__(self, source_directory, work_directory):
        self.source_directory = source_directory
        self.work_directory = work_directory
        self.trainprocessor = TrainProcessor(source_directory, work_directory)
        self.spiral_processor = SpiralProcessor(source_directory, work_directory)

    def process(self, ip, curvetype, station_text, img_f_name, openfile_name, structure):
        tpd = TrainPostData(curvetype=curvetype, station=station_text, cant='0', filename=img_f_name)
        doc = self.trainprocessor.process(tpd)
        try:
            TrainOutputManager.export_png(doc, img_f_name, self.work_directory)
        finally:
            doc.close()
        if curvetype in ['SP', 'PS', 'BC', 'EC']:
            self.spiral_processor.process(ip.radius, img_f_name, structure)
        return CurveOutputService.copy_and_export(self.source_directory, self.work_directory,
                                                  openfile_name, img_f_name, curvetype, ip.radius)
