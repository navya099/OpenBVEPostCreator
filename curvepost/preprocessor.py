from common.info_format import InfoFormat, detect_info_format
from curvepost.bve_curvedata_builder import BVECURVEDATABuilder
from curvepost.c3d_curvedata_builder import CIVIL3DCURVEDATABuilder


class CurvePreprocessor:
    BUILDERS = {
        InfoFormat.BVE: BVECURVEDATABuilder,
        InfoFormat.CIVIL3D: CIVIL3DCURVEDATABuilder,
    }

    @staticmethod
    def get_builder(path):
        """정보 파일 확장자에 맞는 빌더 반환"""
        return CurvePreprocessor.BUILDERS[detect_info_format(path)]()

    @staticmethod
    def remove_duplicate_radius(data):
        filtered_data = []
        previous_radius = None

        for row in data:
            try:
                station, radius, cant = map(float, row)
                station = int(station)
            except ValueError:
                print(f"잘못된 데이터 형식: {row}")
                continue

            if radius != previous_radius:
                filtered_data.append((station, radius, cant))
                previous_radius = radius

        return filtered_data

    @staticmethod
    def process_sections(data):
        sections = []
        current_section = []

        for row in data:
            try:
                station, radius, cant = map(float, row)
                station = int(station)
            except ValueError:
                print(f"잘못된 데이터 형식: {row}")
                continue

            current_section.append((station, radius, cant))

            if radius == 0.0 and current_section:
                sections.append(current_section)
                current_section = []

        return sections
