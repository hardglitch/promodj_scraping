import asyncio
from asyncio import Semaphore
from inspect import stack
from typing import Any, Optional, Sequence, Set
from urllib.parse import unquote

from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal
from aiohttp import ClientError
from bs4 import BeautifulSoup, ResultSet, SoupStrainer

from data.data import CONST
from data.messages import MESSAGES
from modules import db, debug
from modules.shared import CurrentValues


class Link:

    __slots__ = "_counter", "success", "message", "search"

    def __init__(self,
                 message: pyqtBoundSignal,
                 success: pyqtBoundSignal,
                 search: pyqtBoundSignal,
        ):
        if not isinstance(self, Link) or \
           not isinstance(success, pyqtBoundSignal | pyqtSignal) or \
           not isinstance(message, pyqtBoundSignal | pyqtSignal) or \
           not isinstance(search, pyqtBoundSignal | pyqtSignal):
                debug.log(MESSAGES.Errors.NoLinkToDownload + f" in {stack()[0][3]}")
                return

        self.message = message
        self.success = success
        self.search = search
        self._counter: int = 0


    async def get_all_links(self) -> Optional[Set[str]]:
        #1. Get a raw link set
        page_number: int = 1
        found_links: Set[str] = set()
        while  len(found_links) < CurrentValues.quantity and not CurrentValues.is_period\
            or len(found_links) < CONST.MaxValues.quantity and CurrentValues.is_period:

            if page_number > 1 and not found_links: break
            page = Page(page_number)
            if not (link_massive := await page.parse()):
                if debug.Switches.IS_GUI: self.message.emit(MESSAGES.Errors.UnableToConnect)
                return None
            found_links_on_page: Set[str] = self._get_filtered_links(link_massive)

            if not found_links_on_page & found_links: found_links |= found_links_on_page
            else: break
            if debug.Switches.IS_GUI: self.search.emit(page_number % 5, 1)
            page_number += 1

        # 2. Checking found links
        if not found_links:
            if debug.Switches.IS_GUI: self.success.emit(0)
            return None
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
        return found_links if found_links else self.success.emit(0) if debug.Switches.IS_GUI else None

# --------------------------------------------------------------------------

    def _get_filtered_links(self, link_massive: ResultSet) -> Set[str]:
        if not link_massive or not isinstance(link_massive, ResultSet):
            debug.log(MESSAGES.Errors.NoLinksToFiltering)
            if debug.Switches.IS_GUI: self.message.emit(MESSAGES.Errors.NoLinksToFiltering)
            return set()

        formats: Sequence[str] = [*CONST.LOSSLESS_COMPRESSED_FORMATS, *CONST.LOSSLESS_UNCOMPRESSED_FORMATS] \
            if CurrentValues.is_lossless else CONST.LOSSY_FORMATS

        return set(link["href"] for link in link_massive if any(link["href"].endswith(_format)
                    and link["href"].find("/source/", 1) > -1 for _format in formats))


    async def _filtered_found_links(self, found_links: Set[str]) -> Set[str]:
        if not found_links or not isinstance(found_links, Set) \
                or not all(map(lambda x: True if type(x) == str else False, found_links)):
            debug.log(MESSAGES.Errors.NoLinksToDownload + f" in {stack()[0][3]}")
            return set()

        found_links = await db.filter_by_history(found_links) if CurrentValues.is_file_history else found_links

        # Convert {"1.wav", "1.flac", "2.flac", "2.wav"} to ['1.flac', '2.wav']
        return set(".".join(_) for _ in {k:v for k, v in [link.rsplit(".", 1) for link in found_links]}.items())


    async def _get_total_filesize_by_link_list(self, found_links: Set[str]) -> None:
        if not found_links or not isinstance(found_links, Set)\
                or not all(map(lambda x: True if type(x) == str else False, found_links)):
            return debug.log(MESSAGES.Errors.NoLinksToDownload + f" in {stack()[0][3]}")

        sem = asyncio.Semaphore(CONST.INTERNAL_THREADS)
        tasks = [asyncio.ensure_future(self._worker(link, sem)) for link in found_links]
        await asyncio.gather(*tasks)

    @debug.switch(debug.Switches.IS_WORKER)
    async def _worker(self, link: str, sem: Semaphore) -> None:
        if isinstance(link, str) and isinstance(sem, Semaphore):
            async with sem: await self._micro_task(link)

    async def _micro_task(self, link: str) -> None:
        if isinstance(link, str):
            async with CurrentValues.session.get(link, timeout=None, headers={"Connection": "keep-alive"}) as response:
                if response.status != 200:
                    return debug.log(MESSAGES.Errors.SomethingWentWrong + f" in {stack()[0][3]}. {response.status=}")
                await self._nano_task(response.content_length)
                if debug.Switches.IS_GUI: self.search.emit(self._counter % 5, 2)
        else:
            return debug.log(repr(TypeError(MESSAGES.Errors.LinkIsNotAStrType)) + f" in {stack()[0][3]}")

    async def _nano_task(self, content_length: Optional[int]) -> None:
        if type(self) == Link or isinstance(content_length, int):
            CurrentValues.total_size += content_length if content_length else 0
            self._counter += 1


class Page:

    __slots__ = "_link"

    def __init__(self, number: int):
        if not isinstance(self, Page) or not isinstance(number, int) or number <= 0:
            debug.log(MESSAGES.Errors.SomethingWentWrong + f" in {stack()[0][3]}")
            return
        bitrate: str = "lossless" if CurrentValues.is_lossless else "high"
        period: str = f"period=last&period_last={CurrentValues.quantity}d&" if CurrentValues.is_period else ""
        self._link = f"https://promodj.com/{CurrentValues.form}/{CurrentValues.genre}?{period}bitrate={bitrate}&page={number}"


    @debug.switch(debug.Switches.IS_PARSE)
    async def parse(self) -> Optional[ResultSet[Any]]:
        try:
            async with CurrentValues.session.get(self._link, timeout=None, headers={"Connection": "keep-alive"}) as response:
                if response.status != 200:
                    debug.log(MESSAGES.Errors.SomethingWentWrong + f" in {stack()[0][3]}. {response.status=}")
                    return None
                return BeautifulSoup(unquote(await response.read()), "lxml", parse_only=SoupStrainer("a")).findAll(href=True)

        except ClientError as error:
            debug.log(MESSAGES.Errors.UnableToConnect + f" in {stack()[0][3]}. {response.status=}", error)
            return None
