from common.stationmanager import StationManager
from kmpost.kmbuilder import KMObjectBuilder
from kmpost.syntax_factory import KMBVESyntaxFactory
from kmpost.typeresolver import KMPostTypeResolver
from model.stationdata import StationData


class FakeStructures:
    def __init__(self):
        self.reversed = False
        self.applied = None

    def define_bridge_tunnel_at_station(self, sta):
        return '교량' if 1000 <= sta <= 1200 else '토공'

    def apply_after_station_to_structure(self, reverse_start, last_block):
        self.applied = (reverse_start, last_block)

    def reverse(self):
        self.reversed = True


OFFSET = {'토공': (3.3, 0.0), '교량': (3.0, 0.5), '터널': (4.5, 0.0)}


def test_station_manager():
    assert StationManager.to_reverse_station(2000, 100, 500) == 1600
    assert StationManager.format_distance(1234.5) == '1+234.50'
    assert StationManager.format_distance(-5.0) == '-0+005.00'


def test_type_resolver():
    assert KMPostTypeResolver.resolve(2000, 200) == 'km표'
    assert KMPostTypeResolver.resolve(2200, 200) == 'm표'
    assert KMPostTypeResolver.resolve(2250, 200) == ''


def test_km_builder_forward():
    b = KMObjectBuilder(800, 1500, FakeStructures(), '일반철도', OFFSET, 200, 0, False)
    res = b.run()
    assert [(r[0].origin_sta, r[0].after_sta, r[1], r[2]) for r in res] == [
        (800, 800, 'm표', '토공'),
        (1000, 1000, 'km표', '교량'),
        (1200, 1200, 'm표', '교량'),
    ]


def test_km_builder_reverse():
    s = FakeStructures()
    b = KMObjectBuilder(0, 1000, s, '도시철도', OFFSET, 100, 500, True)
    res = b.run()
    assert s.reversed and s.applied == (500, 1000)
    assert res[0][0] == StationData(origin_sta=1000, after_sta=500)
    assert [r[0].after_sta for r in res] == [500 + 100 * i for i in range(10)]
    assert res[5][1] == 'km표'


def test_km_syntax_single_and_double():
    f = KMBVESyntaxFactory(10)
    sta = StationData(origin_sta=1000)
    index, post = f.create(i=2, station=sta, structure='교량', target_directory='D:/BVE/Object/km',
                           track_mode='single', offset=OFFSET, track_index={'main': 0, 'sub': None},
                           track_direction={'main': -1, 'sub': None})
    assert index == '.freeobj(12) km/1000.csv\n'
    assert post == '1000,.freeobj 0;12;-3.0;0.5;0;,;교량\n'
    _, post = f.create(i=0, station=sta, structure='토공', target_directory='x/Object/a/b',
                       track_mode='double', offset=OFFSET, track_index={'main': 0, 'sub': 1},
                       track_direction={'main': 1, 'sub': -1})
    assert post == (',;구조물=토공\n,;하선\n1000,.freeobj 0;10;3.3;0.0;180;\n'
                    ',;상선\n1000,.freeobj 1;10;-3.3;0.0;0;\n')
