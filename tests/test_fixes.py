"""리뷰에서 발견된 버그의 회귀 테스트"""
import pandas as pd
import pytest

from common.file_io import try_read_file
from common.info_format import InfoFormat, detect_info_format
from controller.prerunsetup import PreRunSetup
from controller.state import AppState
from gradepost.c3d_vipdata_builder import C3DVIPDATABuilder
from infrastructure.structuresystem import StructureProcessor
from structurepost.structuregenerator import StructureGenerator


def test_try_read_file_falls_back_to_euc_kr(tmp_path):
    f = tmp_path / 'info.txt'
    f.write_bytes('100,곡선\n'.encode('euc-kr'))
    assert try_read_file(str(f)) == [['100', '곡선']]


def test_detect_info_format():
    assert detect_info_format('a/b.TXT') is InfoFormat.BVE
    assert detect_info_format('b.xlsx') is InfoFormat.CIVIL3D
    with pytest.raises(ValueError):
        detect_info_format('b.csv')


def test_effective_brokenchain():
    s = AppState(brokenchain=12.5)
    assert s.effective_brokenchain == 0.0
    s.isbrokenchain = True
    assert s.effective_brokenchain == 12.5


def test_structure_processor_with_empty_tunnel_sheet(tmp_path):
    path = tmp_path / 's.xlsx'
    with pd.ExcelWriter(path) as w:
        pd.DataFrame([['A교', 100, 200, 100]]).to_excel(w, sheet_name='교량', header=False, index=False)
        pd.DataFrame([['dummy']]).to_excel(w, sheet_name='터널', header=False, index=False)
    sp = StructureProcessor(str(path))
    sp.process_structure(10)
    assert sp.define_bridge_tunnel_at_station(205) == '교량'
    assert sp.define_bridge_tunnel_at_station(250) == '토공'


def test_c3d_builder_keeps_last_vip(tmp_path):
    path = tmp_path / 'v.xlsx'
    cols = ['번호', 'PVI 측점', '종단 진입부 경사', '종단 진출부 경사', '종단 원곡선 유형', '종단 원곡선 길이', '원곡선 반지름']
    pd.DataFrame([[1, 100, 0, 5, '오목형', 40, 8000], [2, 500, 5, -3, '볼록형', 60, 7500]],
                 columns=cols).to_excel(path, index=False)
    vips = C3DVIPDATABuilder().build(str(path), 0)
    assert [v.VIP_STA for v in vips] == [100, 500]
    assert (vips[1].BVC_STA, vips[1].EVC_STA) == (470, 530)


class FakeDialogs:
    def __init__(self, *answers):
        self.answers = list(answers)

    def select_option_list(self, options):
        return self.answers.pop(0)


def _ready_state(**kw):
    s = AppState(target_directory='t', structure_excel_path='s.xlsx', offset={'토공': (0, 0)},
                 track_mode='single', track_direction={'main': -1}, track_index={'main': 0})
    for k, v in kw.items():
        setattr(s, k, v)
    return s


def test_prerun_cancel_returns_false():
    logs = []
    assert PreRunSetup(FakeDialogs(None), _ready_state(), logs.append).run() is False
    assert PreRunSetup(FakeDialogs('일반철도', None), _ready_state(), logs.append).run() is False


def test_prerun_validation():
    logs = []
    state = _ready_state(offset=None)
    assert PreRunSetup(FakeDialogs('일반철도', '거리표'), state, logs.append).run() is False
    assert '오프셋 설정' in logs[-1]
    state = _ready_state()
    assert PreRunSetup(FakeDialogs('고속철도', '곡선표'), state, logs.append).run() is False
    assert 'INFO 파일' in logs[-1]
    state = _ready_state(info_path='a.txt')
    assert PreRunSetup(FakeDialogs('고속철도', '곡선표'), state, logs.append).run() is True
    assert (state.alignment_type, state.posttype) == ('고속철도', '곡선표')


def test_structure_generator_constructible():
    logs = []
    StructureGenerator(AppState(), logs.append).generate()
    assert '지원되지 않습니다' in logs[-1]


def test_base_generator_template_flow(tmp_path):
    from common.base_generator import BaseObjectGenerator
    from config import GeneratorPaths

    src = tmp_path / 'src' / '일반철도'
    src.mkdir(parents=True)
    (src / 'a.png').write_bytes(b'x')
    (src / 'b.dxf').write_bytes(b'x')
    excel = tmp_path / 's.xlsx'
    with pd.ExcelWriter(excel) as w:
        pd.DataFrame([['A교', 100, 200, 100]]).to_excel(w, sheet_name='교량', header=False, index=False)
        pd.DataFrame([['B터널', 300, 400, 100]]).to_excel(w, sheet_name='터널', header=False, index=False)

    calls = []

    class Dummy(BaseObjectGenerator):
        NAME = '테스트'

        def build(self):
            calls.append((self.start_sta, self.end_sta, self.structure_processor.define_bridge_tunnel_at_station(355)))
            return ['r']

        def output_files(self, results):
            calls.append(results)

    state = AppState(start_station=0, end_station=1000, brokenchain=50, isbrokenchain=True,
                     alignment_type='일반철도', structure_excel_path=str(excel))
    logs = []
    Dummy(state, logs.append, GeneratorPaths(str(tmp_path / 'src'), str(tmp_path / 'work'))).generate()
    assert calls == [(50, 1050, '터널'), ['r']], logs
    assert sorted(p.name for p in (tmp_path / 'work').iterdir()) == ['a.png']
    assert logs[-1] == '모든 작업이 완료됐습니다.'
