import asyncio
from pathlib import Path

import pytest
from PyQt6.QtCore import pyqtSignal
from aiohttp import StreamReader, streams
from asyncmock import AsyncMock

from modules import debug
from modules.file import File
from modules.shared import CurrentValues
from util.tools import byte_dumb

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

link = "https://promodj.com/some_beautiful_track.flac"

def test_set_wrong_attributes() -> None:
    try: File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int], new=1)
    except: assert TypeError
    try: File(progress=progress[int], message=message[str], file_info=file_info[int, int])
    except: assert ValueError
    try: File()
    except: assert ValueError


def test_types() -> None:
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
    assert isinstance(file, File)
    assert isinstance(file._link, str)
    assert isinstance(file._name, str)
    assert isinstance(file._path, Path)


def test_check_path_and_name(tmp_path) -> None:
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


@pytest.mark.asyncio
async def test_write_file_from_stream(tmp_path) -> None:
    CurrentValues.download_dir = str(tmp_path)
    file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
    debug.Switches.IS_PRINTING = False
    debug.Switches.IS_GUI.value = False
    assert await file._write_file(await _fake_stream())
    file._path.unlink()

async def _fake_stream() -> StreamReader:
    protocol = AsyncMock(_reading_paused=False)
    stream = streams.StreamReader(protocol, 16144, loop=asyncio.get_event_loop())
    stream.feed_data(byte_dumb(200))
    stream.feed_eof()
    return stream
