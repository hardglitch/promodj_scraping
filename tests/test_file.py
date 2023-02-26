from pathlib import Path

from PyQt6.QtCore import pyqtSignal

from modules.file import File

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

link = "https://promodj.com/some_beautiful_track.flac"


def test_set_attribute():
    try:
        File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int], new=1)
    except:
        assert TypeError


def test_values():
    try:
        File(progress=progress[int], message=message[str], file_info=file_info[int, int])
        File()
    except:
        assert ValueError


def test_types():
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])

    assert isinstance(file, File)
    assert isinstance(file._link, str)
    assert isinstance(file._name, str)
    assert isinstance(file._path, Path)
