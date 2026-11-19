import pytest

from curvepost.bve_curvedata_builder import BVECURVEDATABuilder
from curvepost.curve_output_manager import CURVEOutputManager
from curvepost.curve_util import CurveDirection, get_curve_lines
from curvepost.preprocessor import CurvePreprocessor
from gradepost.bve_vipdata_builder import BVEVIPDATABuilder
from gradepost.grade_output_manager import GradeOutputManager
from gradepost.pitch_util import format_grade, get_vcurve_lines
from gradepost.preprocessor import VIPPreprocessor
from model.curve.curve_object_data import CurveObjectDATA
from model.grade.vip_object_data import VIPObjectDATA

OFFSET = {'토공': (3.3, 0.0), '교량': (3.0, 0.5), '터널': (4.5, 0.0)}

CURVE_ROWS = [
    ['0', '0', '0'],
    ['100', '-600', '50'], ['200', '-400', '80'], ['300', '-600', '50'], ['400', '0', '0'],
    ['500', '800', '60'], ['700', '0', '0'],
]


def test_curve_preprocess_and_build():
    rows = CurvePreprocessor.remove_duplicate_radius(CURVE_ROWS)
    sections = CurvePreprocessor.process_sections(rows)
    assert sections[0] == [(0, 0.0, 0.0)]
    ips = BVECURVEDATABuilder().build(sections, 10)
    assert len(ips) == 2
    spiral, circle = ips
    assert spiral.curvetype == '완화곡선' and spiral.curve_direction == CurveDirection.LEFT
    assert (spiral.radius, spiral.cant) == (400, 80)
    assert (spiral.SP_STA, spiral.PC_STA, spiral.CP_STA, spiral.PS_STA) == (110, 210, 310, 410)
    assert circle.curvetype == '원곡선' and circle.curve_direction == CurveDirection.RIGHT
    assert (circle.IPNO, circle.radius, circle.BC_STA, circle.EC_STA) == (2, 800, 510, 710)
    assert get_curve_lines(circle) == [['BC', 510], ['EC', 710]]


def test_curve_flag():
    assert isinstance(CurvePreprocessor.get_builder('a.TXT'), BVECURVEDATABuilder)
    with pytest.raises(ValueError):
        CurvePreprocessor.get_builder('a.csv')


def test_grade_preprocess_and_build():
    rows = [['0', '0.002'], ['10', '0.002'], ['20', '0.004'], ['200', '-0.003'], ['210', '-0.001'],
            ['220', '0.001']]
    lines = VIPPreprocessor.remove_duplicate_pitch(rows)
    sections = VIPPreprocessor.create_sections(lines)
    assert sections == [[(0.0, 0.002), (20.0, 0.004)], [(200.0, -0.003), (210.0, -0.001), (220.0, 0.001)]]
    vips = BVEVIPDATABuilder().build(sections, 5)
    assert [v.isvcurve for v in vips] == [False, True]
    v = vips[1]
    assert (v.BVC_STA, v.VIP_STA, v.EVC_STA, v.seg) == (205, 215, 225, '오목형')
    assert v.vradius == pytest.approx(20 / 0.004)
    assert get_vcurve_lines(vips[0]) == [['VIP', 15.0]]
    assert format_grade(-0.0125) == '-12.5' and format_grade(0.003) == '3'


def _curve_obj():
    return CurveObjectDATA(no=3, curvetype='BC', structure='교량', station=1500, object_index=7,
                           filename='IP3_BC', object_path='curve', offset=(3.0, 0.5))


def _vip_obj():
    return VIPObjectDATA(no=2, vcurve_type='VIP', structure='토공', station=900, object_index=8,
                         filename='VIP2_VIP', object_path='pitch', offset=(3.3, 0.0))


def test_curve_post_text():
    m = CURVEOutputManager('w', 't', OFFSET, 'single', {'main': -1, 'sub': None}, {'main': 0, 'sub': None})
    assert m.create_curve_post_txt([_curve_obj()]) == ['1500,.freeobj 0;7;-3.0;0.5;0;,;IP3_BC-교량\n']
    m = CURVEOutputManager('w', 't', OFFSET, 'double', {'main': 1, 'sub': -1}, {'main': 0, 'sub': 1})
    assert m.create_curve_post_txt([_curve_obj()]) == [
        '1500,.freeobj 0;7;3.0;0.5;180;,;IP3하_BC-교량\n',
        '1500,.freeobj 1;7;-3.0;0.5;0;,;IP3상_BC-교량\n',
    ]


def test_grade_post_text(tmp_path):
    m = GradeOutputManager('w', 't', OFFSET, 'single', {'main': 1, 'sub': None}, {'main': 2, 'sub': None})
    assert m.create_pitch_post_txt([_vip_obj()]) == ['900,.freeobj 2;8;3.3;0.0;180;,;VIP2_VIP-토공\n']
    out = tmp_path / 'idx.txt'
    m.create_pitch_index_txt([_vip_obj()], str(out))
    assert out.read_text(encoding='utf-8') == '.freeobj(8) pitch/VIP2_VIP.csv\n'
