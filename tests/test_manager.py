import asyncio
import sys
from concurrent.futures import Future

import allure
import pytest
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtWidgets import QApplication
from aiohttp import ClientSession
from qasync import QEventLoop

from data.data import Data
from modules import debug
from modules.gui import MainWindow
from modules.manager import Manager
from modules.shared import CurrentValues
from util import tools


@allure.epic("Test the Manager values and types")
class TestManager:

    @pytest.fixture(scope="function")
    def setup(self) -> Manager:
        self._test_app = QApplication(sys.argv)
        self._test_loop: asyncio.AbstractEventLoop = QEventLoop(self._test_app)
        asyncio.set_event_loop(self._test_loop)
        MainWindow()
        return Manager(
            download_dir=Data.DefaultValues.download_dir,
            genre=Data.DefaultValues.genre,
            form=Data.DefaultValues.form,
            is_lossless=Data.DefaultValues.is_lossless,
            quantity=Data.DefaultValues.quantity,
            is_period=Data.DefaultValues.is_period,
            threads=Data.DefaultValues.threads,
            is_rewrite_files=Data.DefaultValues.is_rewrite_files,
            is_file_history=Data.DefaultValues.is_file_history
        )

    def test_default_values(self, setup) -> None:
        mng = setup
        assert CurrentValues.download_dir == Data.DefaultValues.download_dir
        assert CurrentValues.genre == Data.DefaultValues.genre
        assert CurrentValues.form == Data.DefaultValues.form
        assert CurrentValues.is_lossless == Data.DefaultValues.is_lossless
        assert CurrentValues.quantity == Data.DefaultValues.quantity
        assert CurrentValues.is_period == Data.DefaultValues.is_period
        assert CurrentValues.threads == Data.DefaultValues.threads
        assert CurrentValues.is_rewrite_files == Data.DefaultValues.is_rewrite_files
        assert CurrentValues.is_file_history == Data.DefaultValues.is_file_history

        assert mng._downloading is None
        assert CurrentValues.session is None

        assert mng.progress[int]
        assert mng.success[int]
        assert mng.search[int, int]
        assert mng.message[str]
        assert mng.file_info[int, int]

        assert CurrentValues.total_files == 0
        assert CurrentValues.total_downloaded_files == 0
        assert CurrentValues.total_downloaded == 0
        assert CurrentValues.total_size == 0


    def test_default_types(self, setup) -> None:
        mng = setup
        assert isinstance(CurrentValues.download_dir, str)
        assert isinstance(CurrentValues.genre, str)
        assert isinstance(CurrentValues.form, str)
        assert isinstance(CurrentValues.is_lossless, bool)
        assert isinstance(CurrentValues.quantity, int)
        assert isinstance(CurrentValues.is_period, bool)
        assert isinstance(CurrentValues.threads, int)
        assert isinstance(CurrentValues.is_rewrite_files, bool)
        assert isinstance(CurrentValues.is_file_history, bool)

        assert isinstance(mng._downloading, Future | None)
        assert isinstance(CurrentValues.session, ClientSession | None)

        assert isinstance(mng.progress[int], pyqtBoundSignal)
        assert isinstance(mng.success[int], pyqtBoundSignal)
        assert isinstance(mng.search[int, int], pyqtBoundSignal)
        assert isinstance(mng.message[str], pyqtBoundSignal)
        assert isinstance(mng.file_info[int, int], pyqtBoundSignal)

        assert isinstance(CurrentValues.total_files, int)
        assert isinstance(CurrentValues.total_downloaded_files, int)
        assert isinstance(CurrentValues.total_downloaded, int)
        assert isinstance(CurrentValues.total_size, int)


@allure.epic("Test the Manager implementation")
class TestManagerAsyncio:

    @pytest.fixture(scope="function")
    def setup(self) -> Manager:
        self._test_app = QApplication(sys.argv)
        return Manager(
            download_dir=Data.DefaultValues.download_dir,
            genre=Data.DefaultValues.genre,
            form=Data.DefaultValues.form,
            is_lossless=Data.DefaultValues.is_lossless,
            quantity=Data.DefaultValues.quantity,
            is_period=Data.DefaultValues.is_period,
            threads=Data.DefaultValues.threads,
            is_rewrite_files=Data.DefaultValues.is_rewrite_files,
            is_file_history=Data.DefaultValues.is_file_history
        )

    @pytest.mark.asyncio
    async def test_manager_init_bruteforce(self) -> None:
        assert await tools.fuzzer(Manager.__init__, hard_mode=debug.Switches.IS_HARD_MODE)


    @pytest.mark.asyncio
    async def test_get_files_negative(self, setup) -> None:
        def fake_get_all_files_none():
            return None

        mng = setup
        debug.Switches.IS_GUI = False
        CurrentValues.is_file_history = False

        CurrentValues.session = None
        assert not await mng._get_files()
        debug.Switches.IS_GET_ALL_FILES.fake_func = fake_get_all_files_none
        assert not await mng._get_files()


    @pytest.mark.asyncio
    async def test_get_files_positive(self, setup) -> None:
        def fake_get_all_files_result():
            return {"link1.flac", "link2.wav", "link3.aiff"}

        mng = setup
        debug.Switches.IS_GUI = False
        CurrentValues.is_file_history = False

        CurrentValues.session = ClientSession(timeout=None, headers={"Connection": "keep-alive"})
        debug.Switches.IS_GET_ALL_FILES.fake_func = fake_get_all_files_result
        debug.Switches.IS_BALANCER.value = False

        assert not await mng._get_files()
        assert CurrentValues.total_files == 3
