from pathlib import Path

from PyQt6.QtCore import pyqtSignal

from modules.file import File
from modules.shared import CurrentValues

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

link = "https://promodj.com/some_beautiful_track.flac"


def test_set_wrong_attributes():
    try:
        File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int], new=1)
    except:
        assert TypeError
    try:
        File(progress=progress[int], message=message[str], file_info=file_info[int, int])
    except:
        assert ValueError
    try:
        File()
    except:
        assert ValueError



def test_types():
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])

    assert isinstance(file, File)
    assert isinstance(file._link, str)
    assert isinstance(file._name, str)
    assert isinstance(file._path, Path)


def test_check_path_and_name(tmp_path):
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])

    # 1. file not exists
    pre_name = file._name
    pre_path = file._path
    file._check_path_and_name()
    assert pre_name == file._name
    assert pre_path == file._path

    # 2. file exists
    CurrentValues.download_dir = str(tmp_path)
    CurrentValues.is_rewrite_files = False
    CurrentValues.is_file_history = False
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
    with open(file._path, "wb") as _file: _file.write(b"")

    pre_name = file._name
    pre_path = file._path
    file._check_path_and_name()
    assert isinstance(file._name, str)
    assert isinstance(file._path, Path)
    assert pre_name != file._name
    assert pre_path != file._path

    pre_path.unlink()