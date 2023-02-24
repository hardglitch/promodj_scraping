import asyncio
from inspect import stack
from typing import Dict, List, Optional, Set
from urllib.parse import unquote

from PyQt6.QtCore import pyqtSignal
from aiohttp import ClientError
from bs4 import BeautifulSoup, ResultSet, SoupStrainer

from data.data import CONST
from data.messages import MESSAGES
from modules import db, debug
from modules.shared import CurrentValues
from util import tools


class Link:
    def __init__(self,
                 message: pyqtSignal(str),
                 success: pyqtSignal(int),
                 search: pyqtSignal(int, int),
        ):
        self.message = message
        self.success = success
        self.search = search
        self._counter: int = 0


    async def get_all_links(self) -> Set[str]:
        #1. Get a raw link set
        page_number: int = 1
        found_links: Set[str] = set()
        while  len(found_links) < CurrentValues.quantity and not CurrentValues.is_period\
            or len(found_links) < CONST.MaxValues.quantity and CurrentValues.is_period:

            if page_number > 1 and not found_links: break
            page = Page(page_number)
            link_massive = await page.parse()
            if not link_massive:
                self.message[str].emit(MESSAGES.Errors.UnableToConnect)
                return set()
            found_links_on_page: Set[str] = self._get_filtered_links(link_massive)

            if not found_links_on_page & found_links: found_links |= found_links_on_page
            else: break
            self.search[int, int].emit(page_number % 5, 1)
            page_number += 1

        # 2. Checking found links
        if not found_links: return self.success[int].emit(0)
        else:
            found_links = \
                set(list(found_links)[:CurrentValues.quantity]) if not CurrentValues.is_period \
                else set(list(found_links)[:CONST.MaxValues.quantity]) if len(found_links) > CONST.MaxValues.quantity \
                else found_links

        # 3. Filtering found links
        found_links = await self._filtered_found_links(found_links)

        # 4. Choosing an algorithm for indicating the GUI download process
        if 0 < len(found_links) < CONST.DefaultValues.file_threshold:
            await self._get_total_filesize_by_link_list(found_links)

        # 5. Return result
        return found_links if found_links else self.success[int].emit(0)

# --------------------------------------------------------------------------

    def _get_filtered_links(self, link_massive: ResultSet) -> Set[str]:
        if not link_massive:
            debug.log(MESSAGES.Errors.NoLinksToFiltering)
            self.message[str].emit(MESSAGES.Errors.NoLinksToFiltering)
        assert isinstance(link_massive, ResultSet)

        filtered_links: Set = set()
        formats: List[str] = [*CONST.LOSSLESS_COMPRESSED_FORMATS, *CONST.LOSSLESS_UNCOMPRESSED_FORMATS] \
            if CurrentValues.is_lossless else CONST.LOSSY_FORMATS

        [[filtered_links.add(tools.clear_path(link["href"])) for _format in formats
            if link["href"].endswith(_format) and link["href"].find("/source/", 1) > -1] for link in link_massive]

        return filtered_links


    async def _filtered_found_links(self, found_links: Set[str]) -> Set[str]:
        if not found_links:
            debug.log(MESSAGES.Errors.NoLinksToDownload + f" in {stack()[0][3]}")
            return set()

        found_links = await db.filter_by_history(found_links) if CurrentValues.is_file_history else found_links

        # Convert {"1.wav", "1.flac", "2.flac", "2.wav"} to ['1.flac', '2.wav']
        tmp_dict: Dict[str, str] = {}
        [[tmp_dict.update({n[0]: n[1]}) for n in [link.rsplit(".", 1)]] for link in found_links]
        f_links: List[str] = []
        [f_links.append(".".join(_)) for _ in tmp_dict.items()]
        # --------------------------------------------
        return set(f_links)



    async def _get_total_filesize_by_link_list(self, f_links: Set[str]) -> None:
        if not f_links: return debug.log(MESSAGES.Errors.NoLinksToDownload + f" in {stack()[0][3]}")
        assert isinstance(f_links, Set)
        assert all(map(lambda x: True if type(x) == str else False, f_links))

        sem = asyncio.Semaphore(CONST.INTERNAL_THREADS)
        tasks = [asyncio.ensure_future(self._worker(link, sem)) for link in f_links]
        await asyncio.gather(*tasks)

    async def _worker(self, link: str, sem: asyncio.Semaphore):
        async with sem: await self._micro_task(link)

    async def _micro_task(self, link: str) -> None:
        async with CurrentValues.session.get(link, timeout=None, headers={"Connection": "keep-alive"}) as response:
            if response.status != 200:
                return debug.log(MESSAGES.Errors.SomethingWentWrong + f" in {stack()[0][3]}. {response.status=}")
            CurrentValues.total_size += response.content_length if response.content_length else 0
            self._counter += 1
            self.search[int, int].emit(self._counter % 5, 2)



class Page:
    def __init__(self, number: int):
        bitrate: str = "lossless" if CurrentValues.is_lossless else "high"
        period: str = f"period=last&period_last={CurrentValues.quantity}d&" if CurrentValues.is_period else ""
        self._link = f"https://promodj.com/{CurrentValues.form}/{CurrentValues.genre}?{period}bitrate={bitrate}&page={number}"

    async def parse(self) -> Optional[ResultSet]:
        try:
            async with CurrentValues.session.get(self._link, timeout=None, headers={"Connection": "keep-alive"}) as response:
                if response.status != 200: return None
                return BeautifulSoup(unquote(await response.read()), "lxml", parse_only=SoupStrainer("a")).findAll(href=True)

        except ClientError as error:
            return debug.log(MESSAGES.Errors.UnableToConnect, error)
