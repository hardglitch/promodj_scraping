from inspect import stack
from typing import List, Set
from urllib.parse import unquote

from PyQt6.QtCore import pyqtSignal
from aiohttp import ClientError
from bs4 import BeautifulSoup, ResultSet

from modules import db, debug
from modules.data import Data
from modules.facade import CurrentValues
from modules.messages import Messages
from modules.pool import Pool, Task


class Link:
    def __init__(self,
                 message: pyqtSignal(str),
                 success: pyqtSignal(int),
                 search: pyqtSignal(int, int),
        ):
        self._links: List = []
        self.message = message
        self.success = success
        self.search = search


    def _get_filtered_links(self, links_massive: ResultSet) -> Set[str]:
        if not links_massive:
            debug.log(Messages.Errors.NoLinksToFiltering)
            self.message[str].emit(Messages.Errors.NoLinksToFiltering)
        assert isinstance(links_massive, ResultSet)

        filtered_links = set()
        formats: List[str] = [*Data.LOSSLESS_COMPRESSED_FORMATS, *Data.LOSSLESS_UNCOMPRESSED_FORMATS] \
            if CurrentValues.is_lossless else Data.LOSSY_FORMATS
        for link in links_massive:
            for frmt in formats:
                if link.has_attr("href") and link["href"].find(frmt) > -1 and link["href"].find("/source/") > -1:
                    filtered_links.add(link["href"])
        return filtered_links


    async def get_all_links(self) -> List[str]:
        if not CurrentValues.session:
            debug.log(Messages.Errors.UnableToDownload)
            self.message[str].emit(Messages.Errors.UnableToDownload)
            return []

        page: int = 1
        found_links: Set[str] = set()
        bitrate: str = "lossless" if CurrentValues.is_lossless else "high"
        period: str = f"period=last&period_last={CurrentValues.quantity}d&" if CurrentValues.is_period else ""
        while \
                len(found_links) < CurrentValues.quantity and not CurrentValues.is_period\
                or CurrentValues.is_period and len(found_links) < Data.MaxValues.quantity:

            if page > 1 and not found_links: break
            link = f"https://promodj.com/{CurrentValues.form}/{CurrentValues.genre}?{period}bitrate={bitrate}&page={page}"
            try:
                async with CurrentValues.session.get(link, timeout=None,
                                                     headers={"Connection": "keep-alive"}) as response:
                    if response.status != 200: break
                    text = str(await response.read())
                    links = BeautifulSoup(unquote(text), features="html.parser").findAll("a")

                    found_links_on_page: set = self._get_filtered_links(links)
                    assert isinstance(found_links_on_page, Set)

                    if not found_links_on_page & found_links:
                        found_links |= found_links_on_page
                    else: break
                    self.search[int, int].emit(page % 5, 1)
                    page += 1

            except ClientError as error:
                debug.log(Messages.Errors.UnableToConnect, error)
                self.message[str].emit(Messages.Errors.UnableToConnect)

        if not found_links:
            self.success[int].emit(0)
            return []

        found_links = await db.filter_by_history(found_links) if CurrentValues.is_file_history else found_links

        # Convert {"1.wav", "1.flac", "2.flac", "2.wav"} to ['1.flac', '2.wav']
        tmp_dict = {}
        [tmp_dict.update({link.rsplit(".", 1)[0]: link.rsplit(".", 1)[1]}) for link in found_links]
        [self._links.append(".".join(_)) for _ in tmp_dict.items()]
        # --------------------------------------------

        self._links = self._links[:CurrentValues.quantity] \
            if not CurrentValues.is_period \
            else self._links[:Data.MaxValues.quantity]

        if 0 < len(self._links) < Data.DefaultValues.file_threshold:
            await self._get_total_filesize_by_link_list()

        return self._links if self._links else self.success[int].emit(0)


    async def _get_total_filesize_by_link_list(self):
        if not self._links: debug.log(Messages.Errors.NoLinksToDownload + f" in {stack()[0][3]}")
        assert isinstance(self._links, List)
        assert all(map(lambda x: True if type(x) == str else False, self._links))

        pool = Pool()
        for link in self._links: await pool.put(Task(micro_link=link, search=self.search))
        await pool.start()
        await pool.join()
