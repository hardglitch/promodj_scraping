import asyncio
from pathlib import Path

import aiofiles
import allure
from PyQt6.QtCore import pyqtSignal
from aiohttp import StreamReader, streams
from asyncmock import AsyncMock

from modules import debug
from modules.file import File
from modules.shared import CurrentValues
from util import tools
from util.tools import byte_dumb

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

link = "https://promodj.com/some_beautiful_track.flac"
debug.Switches.IS_GUI = False


@allure.epic("All transactions with files")
class TestFile:

    @allure.description("Bruteforce File method")
    async def test_file_init_bruteforce(self):
        assert await tools.fuzzer(File.__init__, hard_mode=debug.Switches.IS_HARD_MODE)

    @allure.description("Bruteforce File instance")
    def test_set_attribute(self):
        file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
        debug.set_attribute_test(file)

    @allure.description("Bruteforce File instance")
    def test_set_wrong_attributes(self) -> None:
        try: File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int], new=1)
        except: assert TypeError
        try: File(progress=progress[int], message=message[str], file_info=file_info[int, int])
        except: assert ValueError
        try: File()
        except: assert ValueError

    @allure.description("Test types of File attributes")
    def test_types(self) -> None:
        file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
        assert isinstance(file, File)
        assert isinstance(file._link, str)
        assert isinstance(file._name, str)
        assert isinstance(file._path, Path)

    @allure.description("Test File method")
    def test_check_path_and_name_1(self, tmp_path) -> None:
        # 1. file not exists
        CurrentValues.download_dir = str(tmp_path)
        file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])

        pre_name = file._name
        pre_path = file._path
        file._check_path_and_name()
        assert pre_name == file._name
        assert pre_path == file._path

    @allure.description("Test File method")
    async def test_check_path_and_name_2(self, tmp_path) -> None:
        # 2. file exists
        CurrentValues.download_dir = str(tmp_path)
        CurrentValues.is_rewrite_files = False
        CurrentValues.is_file_history = False
        file = File(link=link+"1", progress=progress[int], message=message[str], file_info=file_info[int, int])
        async with aiofiles.open(file._path, "wb") as _file: await _file.write(b"")

        pre_name = file._name
        pre_path = file._path
        file._check_path_and_name()
        assert isinstance(file._name, str)
        assert isinstance(file._path, Path)
        assert pre_name != file._name
        assert pre_path != file._path

        pre_path.unlink()

    @allure.description("Bruteforce File method")
    async def test_check_path_and_name_bruteforce(self):
        file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
        assert await tools.fuzzer(file._check_path_and_name, hard_mode=debug.Switches.IS_HARD_MODE)

    @allure.description("Test File method")
    async def test_write_file_from_stream(self, tmp_path) -> None:
        CurrentValues.download_dir = str(tmp_path)
        file = File(link=link+"2", progress=progress[int], message=message[str], file_info=file_info[int, int])
        debug.Switches.IS_PRINTING = False
        debug.Switches.IS_GUI = False
        assert await file._write_file(await self._fake_stream())
        file._path.unlink()

    async def _fake_stream(self) -> StreamReader:
        protocol = AsyncMock(_reading_paused=False)
        stream = streams.StreamReader(protocol, 16144, loop=asyncio.get_event_loop())
        stream.feed_data(byte_dumb(200))
        stream.feed_eof()
        return stream

    @allure.description("Bruteforce File method")
    async def test_write_file_bruteforce(self):
        file = File(link=link, progress=progress[int], message=message[str], file_info=file_info[int, int])
        assert await tools.fuzzer(file._write_file, hard_mode=debug.Switches.IS_HARD_MODE)
