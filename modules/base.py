import asyncio
import urllib.parse
from asyncio import AbstractEventLoop
from pathlib import Path
from time import time
from typing import AnyStr, Awaitable, List, Set

import aiofiles
import aiohttp
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from bs4 import BeautifulSoup, ResultSet

from modules.data import Data
from modules.messages import Messages


class Base(QMainWindow):

    progress = pyqtSignal(int)
    succeeded = pyqtSignal(int)
    total_size: int = 0
    total_downloaded: int = 0

    def __init__(self,
                 download_dir: AnyStr = Data.DefaultValues.download_dir,
                 genre: AnyStr = Data.DefaultValues.genre,
                 form: AnyStr = Data.DefaultValues.form,
                 is_lossless: bool = Data.DefaultValues.is_lossless,
                 quantity: int = Data.DefaultValues.quantity,
                 is_period: bool = Data.DefaultValues.is_period,
                 is_download: bool = Data.DefaultValues.is_download,
                 threads: int = Data.DefaultValues.threads,
                 is_rewrite_files: bool = Data.DefaultValues.is_rewrite_files,
                 is_file_history: bool = Data.DefaultValues.is_file_history,
                 loop: AbstractEventLoop = None
        ):

        super().__init__()
        self.download_dir: Path = Path(download_dir)
        self.genre: AnyStr = genre
        self.form: AnyStr = form
        self.is_lossless: bool = is_lossless
        self.quantity: int = quantity if quantity < abs(Data.MaxValues.quantity) else abs(Data.MaxValues.quantity)
        self.is_period: bool = is_period
        self.is_download: bool = is_download
        self.threads: int = threads if threads < abs(Data.MaxValues.threads) else abs(Data.MaxValues.threads)
        self.is_rewrite_files: bool = is_rewrite_files
        self.is_file_history: bool = is_file_history

        self._download_future = None
        self._loop: AbstractEventLoop = loop


    @staticmethod
    def print(*args, **kwargs):
        if Data.PRINTING:
            print(*args, **kwargs)

    def get_filtered_links(self, links_massive: ResultSet = None) -> Set[AnyStr]:
        if links_massive is None:
            self.print(Messages.Errors.NoLinksToFiltering)
            exit()

        filtered_links = set()
        formats: list = Data.LOSSLESS_FORMATS if self.is_lossless else Data.LOSSY_FORMATS
        for link in links_massive:
            for frmt in formats:
                if link.has_attr("href") and link["href"].find(frmt) > -1 and link["href"].find("/source/") > -1:
                    filtered_links.add(link["href"])    # deduplication
        return filtered_links


    async def get_all_links(self, session: aiohttp.ClientSession = None) -> List[AnyStr]:
        if session is None:
            self.print(Messages.Errors.UnableToDownload)
            exit()

        page: int = 1
        found_links = set()
        bitrate = "lossless" if self.is_lossless else "high"
        period = f"period=last&period_last={self.quantity}d&" if self.is_period else ""
        while (len(found_links) < self.quantity and not self.is_period) or self.is_period:
            link = f"https://promodj.com/{self.form}/{self.genre}?{period}bitrate={bitrate}&page={page}"
            async with session.get(link) as response:
                if response.status != 200: break
                text = str(await response.read())
                links = BeautifulSoup(urllib.parse.unquote(text), features="html.parser").findAll("a")
                found_links_on_page: set = self.get_filtered_links(links)
                if not found_links_on_page & found_links:
                    found_links |= found_links_on_page
                else:
                    break
                page += 1
        return list(found_links)[:self.quantity] if not self.is_period else list(found_links)


    async def get_total_filesize(self, session: aiohttp.ClientSession = None, links: List[Awaitable] = None):

        async def micro_task(micro_link):
            async with session.get(micro_link) as response:
                if response.status != 200:
                    return self.print(Messages.Errors.SomethingWentWrong)
                self.total_size += response.content_length

        if session is None:
            self.print(Messages.Errors.UnableToConnect)
            exit()

        micro_tasks = []
        for link in links:
            micro_tasks.append(asyncio.ensure_future(micro_task(link)))

        await asyncio.gather(*micro_tasks)

        if len(micro_tasks) == 0:
            self.succeeded.emit(0)


    async def get_file_by_link(self, session: aiohttp.ClientSession = None, link: AnyStr = None):
        if link is None:
            self.print(Messages.Errors.NoLinkToDownload)
            exit()
        if session is None:
            self.print(Messages.Errors.UnableToConnect)
            exit()

        filename: str = link.split("/")[-1]
        ext_time = str(time()).replace(".", "")
        ext_pos = filename.rfind(".")
        filename = filename \
            if Path(Path.joinpath(self.download_dir, filename)).exists() and self.is_rewrite_files \
               or not Path(Path.joinpath(self.download_dir, filename)).exists()\
            else filename[:ext_pos] + "_" + ext_time + filename[ext_pos:]

        if self.is_download:
            async with session.get(link, timeout=None) as response:
                if response.status != 200:
                    return self.print(Messages.Errors.SomethingWentWrong)

                async with aiofiles.open(Path.joinpath(self.download_dir, filename), "wb") as file:
                    self.print(f"Downloading {filename}...\nLink - {link}")

                    chunk_size = 16144
                    async for chunk in response.content.iter_chunked(chunk_size):
                        if not chunk: break
                        self.total_downloaded += chunk_size
                        if self.total_size > 0:
                            self.progress.emit(int(100 * self.total_downloaded / (self.total_size * 1.21)))
                        await file.write(chunk)
        self.print(f"File save as {Path.joinpath(self.download_dir, filename)}")
        # if self.file_history:
        #     await self.open_db()

    # async def open_db(self):
    #     async with aiosqlite.connect("history.db") as db:
    #         if not Path("history.db").exists():
    #             print("1")
    #         else:
    #             print("2")

    async def threads_limiter(self, sem: asyncio.Semaphore = None,
                              session: aiohttp.ClientSession = None, link: Awaitable = None) -> None:
        async with sem:
            return await self.get_file_by_link(session, link)


    async def get_files(self):
        async with aiohttp.ClientSession() as session:
            sem = asyncio.Semaphore(self.threads)
            tasks = []
            all_links = await self.get_all_links(session)

            await self.get_total_filesize(session, all_links)

            for link in all_links:
                tasks.append(asyncio.ensure_future(self.threads_limiter(sem=sem, session=session, link=link)))

            await asyncio.gather(*tasks)

            if len(tasks) > 0:
                self.succeeded.emit(1)
            else:
                self.succeeded.emit(0)


    def start_downloading(self):
        self._download_future = asyncio.run_coroutine_threadsafe(self.get_files(), self._loop)


    def cancel_downloading(self):
        if self._download_future:
            self._loop.call_soon_threadsafe(self._download_future.cancel)