import asyncio
from asyncio import AbstractEventLoop
from typing import Any, Awaitable, List

import aiofiles
import aiohttp
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from bs4 import BeautifulSoup, ResultSet

from .data import Data
from .messages import Messages


class Base(QMainWindow):

    progress = pyqtSignal(int)
    succeeded = pyqtSignal(int)
    total_size: int = 0
    total_downloaded: int = 0

    def __init__(self,
                 download_dir: str = "music",
                 genre: str = "trance",
                 form: str = "tracks",
                 lossless: bool = True,
                 quantity: int = 10,
                 period: bool = False,
                 download: bool = True,
                 threads: int = 4,
                 loop: AbstractEventLoop = None
        ) -> None:

        super().__init__()
        self.download_dir: str = download_dir
        self.genre: str = genre
        self.form: str = form
        self.lossless: bool = lossless
        self.quantity: int = quantity
        self.period: bool = period
        self.download: bool = download
        self.threads: int = threads

        self._file_counter: int = 0
        self._all_files: int = 0
        self._grade: int = 0
        self._download_future = None
        self._loop: AbstractEventLoop = loop


    @staticmethod
    def print(*args, **kwargs):
        if Data.PRINTING:
            print(*args, **kwargs)

    def limiter(self, param: Any) -> Any:
        param = param.lower() if type(param) is str else param
        if param == self.form.lower() and param in Data.FORMS \
                or param == self.genre and param in Data.GENRES.values():
            return param
        if param == self.quantity:
            param = param if param <= abs(Data.MaxValues.quantity) else Data.MaxValues.quantity
            return param
        if param == self.threads:
            param = param if param <= abs(Data.MaxValues.threads) else Data.MaxValues.threads
            return param
        self.print(Messages.Errors.NoSuitableParameter)
        exit()


    def get_filtered_links(self, links_massive: ResultSet = None) -> List[str]:
        if links_massive is None:
            self.print(Messages.Errors.NoLinksToFiltering)
            exit()

        filtered_links: dict = {}
        formats: list = Data.LOSSLESS_FORMATS if self.lossless else Data.LOSSY_FORMATS
        for link in links_massive:
            for frmt in formats:
                if link.has_attr("href") and link["href"].find(frmt) > -1:
                    filtered_links[link["href"]] = 1  # deduplication
        return list(filtered_links.keys())


    async def get_all_links(self, session: aiohttp.ClientSession = None) -> List[Awaitable]:
        if session is None:
            self.print(Messages.Errors.UnableToDownload)
            exit()

        page: int = 1
        found_links: list = []
        quantity = self.limiter(self.quantity)
        genre = self.limiter(self.genre)
        form = self.limiter(self.form)
        bitrate = "lossless" if self.lossless else "high"
        period = f"period=last&period_last={quantity}d&" if self.period else ""

        while len(found_links) < quantity:
            link = f"https://promodj.com/{form}/{genre}?{period}bitrate={bitrate}&page={page}"
            async with session.get(link) as response:
                if response.status != 200: break
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                found_links += self.get_filtered_links(links)
                page += 1
        tmp = {}
        for n in found_links: tmp[n] = 1
        return list(tmp)[:quantity]


    def get_file_name_from_link(self, link: str = None) -> str:
        if link is None:
            self.print(Messages.Errors.NoLinkToExtractAName)
            return ""

        decode_simbols = {"%20": " ", "%28": "(", "%29": ")", "%26": "&", "%23": "#"}

        filename: str = link.split("/")[-1]

        for i in decode_simbols:
            filename = filename.replace(i, decode_simbols[i])

        index = 0
        while index != -1:
            index = filename.find(fr"%")
            smb = filename[index:index + 3]
            filename = filename.replace(fr"{smb:2}", "")

        return filename.strip()


    async def get_total_filesize(self, session: aiohttp.ClientSession = None, links: List[Awaitable] = None):

        async def micro_task(micro_link):
            async with session.get(micro_link) as response:
                if response.status != 200:
                    self.print(Messages.Errors.SomethingWentWrong)
                    return
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


    async def get_file_by_link(self, session: aiohttp.ClientSession = None, link: str = None):
        if link is None:
            self.print(Messages.Errors.NoLinkToDownload)
            exit()
        if session is None:
            self.print(Messages.Errors.UnableToConnect)
            exit()

        filename = self.get_file_name_from_link(link)
        if self.download:
            async with session.get(link, timeout=None) as response:
                if response.status != 200:
                    self.print(Messages.Errors.SomethingWentWrong)
                    return

                async with aiofiles.open(self.download_dir + filename, "wb") as file:
                    self.print(f"Downloading {filename}...\nLink - {link}")

                    chunk_size = 16144   #  8192 / 16384
                    async for chunk in response.content.iter_chunked(chunk_size):
                        if not chunk: break
                        self.total_downloaded += chunk_size
                        self.progress.emit(int(100 * self.total_downloaded / (self.total_size * 1.21)))
                        await file.write(chunk)
        self.print(f"File save as {self.download_dir + filename}")


    async def threads_limiter(self, sem: asyncio.Semaphore = None,
                              session: aiohttp.ClientSession = None, link: Awaitable = None) -> None:
        async with sem:
            return await self.get_file_by_link(session, link)


    async def get_files(self) -> None:
        async with aiohttp.ClientSession() as session:
            sem = asyncio.Semaphore(self.limiter(self.threads))
            tasks = []
            all_links = await self.get_all_links(session)

            await self.get_total_filesize(session, all_links)

            for link in all_links:
                tasks.append(asyncio.ensure_future(self.threads_limiter(sem=sem, session=session, link=link)))

            self._all_files = len(tasks)
            self._grade = 100 // self._all_files

            await asyncio.gather(*tasks)

            if len(tasks) > 0: self.succeeded.emit(1)
            else: self.succeeded.emit(0)


    def start_downloading(self):
        self._download_future = asyncio.run_coroutine_threadsafe(self.get_files(), self._loop)


    def cancel_downloading(self):
        if self._download_future:
            self._loop.call_soon_threadsafe(self._download_future.cancel)