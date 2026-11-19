from common.bve_syntax import freeobj_line, object_folder_from, rotation_for, validate_track_mode


class KMBVESyntaxFactory:
    """거리표 BVE 구문 생성기"""
    def __init__(self, first_index=4025):
        self.first_index = first_index

    def create(self, i, station, structure, target_directory, track_mode, offset, track_index, track_direction):
        index = self.first_index + i
        return (
            self.create_km_index_data(index, station, target_directory),
            self.create_km_post_data(index, station, structure, track_mode, offset, track_index, track_direction)
        )

    @staticmethod
    def create_km_index_data(idx, sta, target_directory):
        return f'.freeobj({idx}) {object_folder_from(target_directory)}/{sta.after_sta}.csv\n'

    @staticmethod
    def create_km_post_data(idx, sta, struc, track_mode, offset, track_index, track_direction):
        validate_track_mode(track_mode)
        x_offset, y = offset[struc]

        def line(track):
            direction = track_direction[track]
            return freeobj_line(sta.origin_sta, track_index[track], idx,
                                direction * x_offset, y, rotation_for(direction))

        if track_mode == 'double':
            return f',;구조물={struc}\n,;하선\n{line("main")},;상선\n{line("sub")}'
        # 단선: 주석을 같은 줄에 붙인다
        direction = track_direction['main']
        return freeobj_line(sta.origin_sta, track_index['main'], idx,
                            direction * x_offset, y, rotation_for(direction), struc)
