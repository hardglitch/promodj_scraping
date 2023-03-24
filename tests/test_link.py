from asyncio import Semaphore
from pathlib import Path
from typing import Set

import aiofiles
import allure
from PyQt6.QtCore import pyqtSignal
from bs4 import BeautifulSoup, ResultSet, SoupStrainer

from modules import debug
from modules.link import Link, Page
from modules.shared import CurrentValues
from util import tools

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

CurrentValues.is_file_history = False
debug.Switches.IS_GUI = False
link = Link(message=progress[int], success=success[int], search=search[int, int])


class FakeLink(Link):
    def __init__(self, content_length: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._content_length = content_length

    async def _worker(self, _link: str, sem: Semaphore) -> None:
        async with sem: await self._nano_task(self._content_length)

@allure.epic("Testing all link operations")
class TestLink:

    @staticmethod
    async def _setup_resultset() -> ResultSet:
        test_page = Path("testpage.html") if Path("testpage.html").exists() else Path("tests").joinpath("testpage.html")
        async with aiofiles.open(test_page, "r", encoding="utf-8") as file: test_page = await file.read()
        return BeautifulSoup(test_page, "lxml", parse_only=SoupStrainer("a")).findAll(href=True)

    @allure.epic("Bruteforce Instances")
    class BruteforceInstance:
        @allure.description("Bruteforce Link instance")
        async def test_link_init_bruteforce(self) -> None:
            assert await tools.fuzzer(Link.__init__, hard_mode=debug.Switches.IS_HARD_MODE)

        @allure.description("Bruteforce Link instance")
        def test_set_attribute_link(self) -> None:
            assert debug.set_attribute_test(link)

        @allure.description("Bruteforce Page instance")
        async def test_page_init_bruteforce(self) -> None:
            assert await tools.fuzzer(Page.__init__, hard_mode=debug.Switches.IS_HARD_MODE)

        @allure.description("Bruteforce Page instance")
        def test_set_attribute_page(self) -> None:
            assert debug.set_attribute_test(Page(1))


    @allure.epic("Full Test filtered_found_links")
    class TestFilteredFoundLinks:
        async def test_filtered_found_links_positive(self) -> None:
            found_links = {"1.flac", "2.flac", "2.wav","1.wav"}
            assert isinstance(found_links, Set)
            assert all(map(lambda x: True if type(x)==str else False, found_links))
            assert await link._filtered_found_links(found_links) in [
                {"1.flac", "2.flac"}, {"1.wav", "2.wav"}, {"1.flac", "2.wav"}, {"1.wav", "2.flac"}]

        async def test_filtered_found_links_legal(self) -> None:
            found_links = set()
            assert await link._filtered_found_links(found_links) == set()

        async def test_filtered_found_links_bruteforce(self) -> None:
            assert await tools.fuzzer(link._filtered_found_links, hard_mode=debug.Switches.IS_HARD_MODE)


    @allure.epic("Full Test get_filtered_links")
    class TestGetFilteredLinks:

        async def test_get_filtered_links_lossless(self) -> None:
            CurrentValues.is_lossless = True
            assert link._get_filtered_links(await TestLink._setup_resultset()) == {
                r"https://promodj.com/source/some1.flac",
                r"https://promodj.com/source/some2.wav",
                r"https://promodj.com/source/some22.aiff",
            }

        async def test_get_filtered_links_lossy_value(self) -> None:
            CurrentValues.is_lossless = False
            assert link._get_filtered_links(await TestLink._setup_resultset()) == {
                r"https://promodj.com/source/some3.mp3"
            }

        async def test_get_filtered_links_lossy_types(self) -> None:
            link_massive = ResultSet(SoupStrainer())
            assert isinstance(link_massive, ResultSet)
            assert link._get_filtered_links(link_massive) == set()

        async def test_get_filtered_links_bruteforce(self) -> None:
            assert await tools.fuzzer(link._get_filtered_links, hard_mode=debug.Switches.IS_HARD_MODE)


    @allure.epic("Full Test get_total_filesize")
    class TestGetTotalFileSize:
        async def test_get_total_filesize_by_link_list(self) -> None:
            found_links = {"1", "2", "3"}
            content_length = 100
            assert isinstance(found_links, Set)
            assert all(map(lambda x: True if type(x) == str else False, found_links))

            _link = FakeLink(message=progress[int], success=success[int], search=search[int, int], content_length=content_length)
            await _link._get_total_filesize_by_link_list(found_links)
            assert CurrentValues.total_size == len(found_links) * content_length

        async def test_get_total_filesize_by_link_list_bruteforce(self) -> None:
            assert await tools.fuzzer(link._get_total_filesize_by_link_list, hard_mode=debug.Switches.IS_HARD_MODE)


    async def test_get_all_links(self) -> None:
        debug.Switches.IS_PARSE.fake_func = TestLink._setup_resultset
        debug.Switches.IS_WORKER.fake_func = self._fake_worker
        CurrentValues.is_file_history = False
        CurrentValues.is_lossless = True

        assert await link.get_all_links() == {
            r"https://promodj.com/source/some1.flac",
            r"https://promodj.com/source/some2.wav",
            r"https://promodj.com/source/some22.aiff",
        }

    def _fake_worker(self) -> None:
        pass
