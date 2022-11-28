from . import utils
from .data import Data
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QMainWindow
from bs4 import BeautifulSoup, ResultSet
from typing import Any
import asyncio
import aiohttp
import aiofiles


class Base(QThread):

    setTotalProgress = pyqtSignal(int)
    setCurrentProgress = pyqtSignal(int)
    succeeded = pyqtSignal()

    def __init__(self,
                 download_dir: str = "music",
                 genre: str = "trance",
                 form: str = "tracks",
                 lossless: bool = True,
                 quantity: int = 10,
                 period: bool = False,
                 download: bool = True,
                 threads: int = 4) -> None:

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
        print("No suitable parameter")
        exit()

    def get_filtered_links(self, links_massive: ResultSet = None) -> list:
        if links_massive is None:
            print("No Links to filtering")
            exit()

        filtered_links: dict = {}
        formats: list = Data.LOSSLESS_FORMATS if self.lossless else Data.LOSSY_FORMATS
        for link in links_massive:
            for frmt in formats:
                if link.has_attr("href") and link["href"].find(frmt) > -1:
                    filtered_links[link["href"]] = 1  # deduplication
        return list(filtered_links.keys())

    async def get_all_links(self, session: aiohttp.ClientSession = None) -> list:
        if session is None:
            print("Unable to download")
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
                if response.status == 404: break
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                found_links += self.get_filtered_links(links)
                page += 1
        tmp = {}
        for n in found_links: tmp[n] = 1
        return list(tmp)[:quantity]

    async def get_file_name_from_link(self, link: str = None) -> str:
        if link is None:
            print("No Link to extract a name")
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

    async def get_file_by_link(self, session: aiohttp.ClientSession = None, link: str = None):
        if link is None:
            print("No Link to download")
            exit()
        if session is None:
            print("Unable to connect")
            exit()

        filename = await self.get_file_name_from_link(link)
        if self.download:
            async with session.get(link) as response:
                if response.status != 200:
                    print("Something went wrong")
                    return
                async with aiofiles.open(self.download_dir + filename, "wb") as file:
                    print(f"Downloading {filename}...")
                    async for data in response.content.iter_chunked(1024):
                        self.setCurrentProgress.emit(self._grade * self._file_counter - self._grade % 2)
                        await file.write(data)
                    self._file_counter += 1
                    if self._file_counter < self._all_files:
                        self.setCurrentProgress.emit(self._grade * self._file_counter)
        print(f"File save as {self.download_dir + filename}")

    async def dl_threads_limiter(self, sem: asyncio.Semaphore = None,
                                 session: aiohttp.ClientSession = None, link: str = None):
        async with sem:
            return await self.get_file_by_link(session, link)

    # @utils.async_timer()
    async def get_files(self):
        async with aiohttp.ClientSession() as session:
            links_future = asyncio.as_completed([self.get_all_links(session)])
            sem = asyncio.Semaphore(self.limiter(self.threads))
            tasks = []
            for links in links_future:
                for link in await links:
                    tasks.append(asyncio.ensure_future(self.dl_threads_limiter(sem, session, link)))
            self._all_files = len(tasks)
            self._grade = 100 % self._all_files
            self.setTotalProgress.emit(self._all_files)
            await asyncio.gather(*tasks)
            self.succeeded.emit()
