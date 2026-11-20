"""대상 디렉터리 통째 삭제 문제 회귀 테스트"""
import os

import pytest

from common.output_manager import BaseOutputManager
from infrastructure.filemanager import FileSystemService


def _manager(work, target):
    return BaseOutputManager(str(work), str(target), None, 'single', None, None)


def _make_work(tmp_path):
    work = tmp_path / 'work'
    work.mkdir()
    (work / 'km_post.txt').write_text('new', encoding='utf-8')
    (work / '1000.csv').write_text('csv', encoding='utf-8')
    (work / '1000.png').write_bytes(b'png')
    (work / 'temp.dxf').write_text('dxf', encoding='utf-8')
    return work


def test_copy_result_keeps_existing_target_files(tmp_path):
    work = _make_work(tmp_path)
    target = tmp_path / 'BVE' / 'Object' / 'km'
    (target / 'sub').mkdir(parents=True)
    (target / 'user_object.csv').write_text('keep', encoding='utf-8')
    (target / 'sub' / 'texture.png').write_bytes(b'keep')
    (target / 'km_post.txt').write_text('old', encoding='utf-8')

    copied, overwritten = _manager(work, target).copy_result_files()

    assert (copied, overwritten) == (3, 1)
    assert (target / 'user_object.csv').read_text(encoding='utf-8') == 'keep'
    assert (target / 'sub' / 'texture.png').read_bytes() == b'keep'
    assert (target / 'km_post.txt').read_text(encoding='utf-8') == 'new'   # 같은 이름은 덮어씀
    assert not (target / 'temp.dxf').exists()                             # 제외 확장자
    assert not work.exists()                                              # 작업 폴더는 정리


def test_copy_result_creates_missing_target(tmp_path):
    work = _make_work(tmp_path)
    target = tmp_path / 'new_target'
    assert _manager(work, target).copy_result_files() == (3, 0)
    assert sorted(os.listdir(target)) == ['1000.csv', '1000.png', 'km_post.txt']


@pytest.mark.parametrize('target_rel', ['work', 'work/inner'])
def test_copy_result_rejects_target_inside_work(tmp_path, target_rel):
    work = _make_work(tmp_path)
    with pytest.raises(ValueError):
        _manager(work, tmp_path / target_rel).copy_result_files()
    assert (work / 'km_post.txt').exists()  # 아무것도 지워지지 않음


def test_copy_result_rejects_empty_target(tmp_path):
    work = _make_work(tmp_path)
    with pytest.raises(ValueError):
        _manager(work, '').copy_result_files()


@pytest.mark.parametrize('path', ['', '   ', os.sep, os.path.expanduser('~')])
def test_reset_directory_refuses_protected_paths(path):
    with pytest.raises(ValueError):
        FileSystemService.reset_directory(path)
    with pytest.raises(ValueError):
        FileSystemService.remove_directory(path)


def test_reset_directory_clears_work_dir(tmp_path):
    work = tmp_path / 'work'
    work.mkdir()
    (work / 'stale.png').write_bytes(b'x')
    FileSystemService.reset_directory(str(work))
    assert work.exists() and not any(work.iterdir())
