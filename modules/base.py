import asyncio
import urllib.parse
from concurrent.futures import Future
from pathlib import Path
from time import time
from typing import Awaitable, List, Optional, Set, Tuple

import aiofiles
import aiohttp
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from bs4 import BeautifulSoup, ResultSet

from modules import db, debug
from modules.data import Data
from modules.messages import Messages


class Base(QMainWindow):

    progress = pyqtSignal(int)
    succeeded = pyqtSignal(int)
    total_size: int = 0
    total_downloaded: int = 0

    def __init__(self,
                 download_dir: str = Data.DefaultValues.download_dir,
                 genre: str = Data.DefaultValues.genre,
                 form: str = Data.DefaultValues.form,
                 is_lossless: bool = Data.DefaultValues.is_lossless,
                 quantity: int = Data.DefaultValues.quantity,
                 is_period: bool = Data.DefaultValues.is_period,
                 threads: int = Data.DefaultValues.threads,
                 is_rewrite_files: bool = Data.DefaultValues.is_rewrite_files,
                 is_file_history: bool = Data.DefaultValues.is_file_history
        ):

        super().__init__()
        self.download_dir: Path = Path(download_dir)
        self.genre: str = genre
        self.form: str = form
        self.is_lossless: bool = is_lossless
        self.quantity: int = quantity if quantity < abs(Data.MaxValues.quantity) else abs(Data.MaxValues.quantity)
        self.is_period: bool = is_period
        self.threads: int = threads if threads < abs(Data.MaxValues.threads) else abs(Data.MaxValues.threads)
        self.is_rewrite_files: bool = is_rewrite_files
        self.is_file_history: bool = is_file_history

        self._downloading: Optional[Future] = None
        self._session: Optional[aiohttp.ClientSession] = None


    def get_filtered_links(self, links_massive: ResultSet) -> Set[str]:
        if not links_massive: debug.log(Messages.Errors.NoLinksToFiltering)
        assert isinstance(links_massive, ResultSet)

        filtered_links = set()
        formats: Tuple = Data.LOSSLESS_FORMATS if self.is_lossless else Data.LOSSY_FORMATS
        for link in links_massive:
            for frmt in formats:
                if link.has_attr("href") and link["href"].find(frmt) > -1 and link["href"].find("/source/") > -1:
                    filtered_links.add(link["href"])    # deduplication
        return filtered_links


    async def get_all_links(self) -> List[str]:
        if not self._session: debug.log(Messages.Errors.UnableToDownload)

        page: int = 1
        found_links: Set[str] = set()
        bitrate: str = "lossless" if self.is_lossless else "high"
        period: str = f"period=last&period_last={self.quantity}d&" if self.is_period else ""
        while (len(found_links) < self.quantity and not self.is_period) or self.is_period:
            link = f"https://promodj.com/{self.form}/{self.genre}?{period}bitrate={bitrate}&page={page}"
            async with self._session.get(link) as response:
                if response.status != 200: break
                text = str(await response.read())
                links = BeautifulSoup(urllib.parse.unquote(text), features="html.parser").findAll("a")

                found_links_on_page: set = self.get_filtered_links(links)
                assert isinstance(found_links_on_page, Set)

                if not found_links_on_page & found_links:
                    found_links |= found_links_on_page
                else: break
                page += 1

        found_links: Set[str] = await db.filter_by_history(found_links) if self.is_file_history else found_links
        return list(found_links)[:self.quantity] if not self.is_period else list(found_links)


    async def get_total_filesize(self, links: List[str]):
        if not links: debug.log(Messages.Errors.NoLinksToDownload)
        assert isinstance(links, List)
        for link in links: assert isinstance(link, str)
        async def micro_task(micro_link: str):
            async with self._session.get(micro_link) as response:
                if response.status != 200: return debug.log(Messages.Errors.SomethingWentWrong)
                self.total_size += response.content_length

        micro_tasks: List[Awaitable] = []
        for link in links: micro_tasks.append(asyncio.ensure_future(micro_task(link)))
        await asyncio.gather(*micro_tasks)
        if not micro_tasks: self.succeeded.emit(0)


    async def get_file_by_link(self, link: str):
        if not link: debug.log(Messages.Errors.NoLinkToDownload)
        assert isinstance(link, str)

        filename: str = link.split("/")[-1]
        ext_time: str = str(time()).replace(".", "")
        ext_pos: int = filename.rfind(".")
        filepath: Path = Path.joinpath(self.download_dir, filename)
        filename: str = filename \
            if Path(filepath).exists() and self.is_rewrite_files and not self.is_file_history \
               or not Path(filepath).exists()\
            else filename[:ext_pos] + "_" + ext_time + filename[ext_pos:]

        @debug.is_download()
        async def download() -> None:
            async with self._session.get(link, timeout=None) as response:
                if response.status != 200: return debug.log(Messages.Errors.SomethingWentWrong)

                async with aiofiles.open(filepath, "wb") as file:
                    debug.print_message(f"Downloading {filename}...\nLink - {link}")

                    chunk_size = 16144
                    async for chunk in response.content.iter_chunked(chunk_size):
                        if not chunk: break
                        self.total_downloaded += chunk_size
                        if self.total_size > 0:
                            self.progress.emit(int(100 * self.total_downloaded / (self.total_size * 1.21)))
                        await file.write(chunk)

        await download()
        debug.print_message(f"File save as {filepath}")

        if self.is_file_history:
            await db.write_file_history(link=link, date=int(time()))


    async def threads_limiter(self, sem: asyncio.Semaphore, link: str) -> None:
        assert isinstance(sem, asyncio.Semaphore) and isinstance(link, str)
        async with sem:
            return await self.get_file_by_link(link)


    async def get_files(self):
        try:
            async with aiohttp.ClientSession() as self._session:
                if self.is_file_history: await db.create_history_db()

                sem = asyncio.Semaphore(self.threads)

                tasks = []
                all_links: List[str] = await self.get_all_links()
                assert isinstance(all_links, List)
                if not all_links: return self.succeeded.emit(0)

                await self.get_total_filesize(all_links)

                for link in all_links:
                    tasks.append(asyncio.ensure_future(self.threads_limiter(sem=sem, link=link)))
                await asyncio.gather(*tasks)

                if tasks: self.succeeded.emit(1)
                else: self.succeeded.emit(0)
        except aiohttp.ClientError as error:
            debug.log(Messages.Errors.UnableToConnect, error)


    def start_downloading(self):
        self._downloading = asyncio.run_coroutine_threadsafe(self.get_files(), asyncio.get_event_loop())

    def cancel_downloading(self):
        if self._downloading:
            asyncio.get_event_loop().call_soon_threadsafe(self._downloading.cancel)
