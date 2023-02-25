import asyncio
from asyncio import Semaphore, Task
from concurrent.futures import Future
from typing import List, Optional, Set

from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from aiohttp import ClientSession

from data.data import CONST
from modules import db
from modules.file import File
from modules.link import Link
from modules.shared import CurrentValues


class Manager(QMainWindow):

    progress = pyqtSignal(int)
    success = pyqtSignal(int)
    search = pyqtSignal(int, int)
    message = pyqtSignal(str)
    file_info = pyqtSignal(int, int)

    def __init__(self,
                 download_dir: str = CONST.DefaultValues.download_dir,
                 genre: str = CONST.DefaultValues.genre,
                 form: CONST.DefaultValues.FORMS = CONST.DefaultValues.form,
                 is_lossless: bool = CONST.DefaultValues.is_lossless,
                 quantity: int = CONST.DefaultValues.quantity,
                 is_period: bool = CONST.DefaultValues.is_period,
                 threads: int = CONST.DefaultValues.threads,
                 is_rewrite_files: bool = CONST.DefaultValues.is_rewrite_files,
                 is_file_history: bool = CONST.DefaultValues.is_file_history
        ):

        super().__init__()
        CurrentValues.download_dir = download_dir
        CurrentValues.genre = genre
        CurrentValues.form = form
        CurrentValues.is_lossless = is_lossless
        CurrentValues.quantity = quantity \
            if 0 < quantity <= abs(CONST.MaxValues.quantity) \
            else abs(CONST.DefaultValues.quantity)
        CurrentValues.is_period = is_period
        CurrentValues.threads = threads \
            if 0 < threads <= abs(CONST.MaxValues.threads) \
            else abs(CONST.DefaultValues.threads)
        CurrentValues.is_rewrite_files = is_rewrite_files
        CurrentValues.is_file_history = is_file_history

        CurrentValues.session = None

        CurrentValues.total_files = 0
        CurrentValues.total_downloaded_files = 0
        CurrentValues.total_downloaded = 0
        CurrentValues.total_size = 0

        self._downloading: Optional[Future] = None
        self._success: pyqtBoundSignal = self.success[int]
        self._search: pyqtBoundSignal = self.search[int, int]


    async def _get_files(self) -> None:
        async with CurrentValues.session:
            if CurrentValues.is_file_history: await db.create_history_db()

            link: Link = Link(message=self.progress[int], success=self.success[int], search=self.search[int, int])
            all_links: Optional[Set[str]] = await link.get_all_links()
            if not all_links: return self._success.emit(0)
            # assert isinstance(all_links, Set)
            # assert all(map(lambda x: True if type(x)==str else False, all_links))

            sem = Semaphore(CurrentValues.threads)
            tasks: List[Task] = [asyncio.ensure_future(self._worker(_link, sem)) for _link in all_links]
            CurrentValues.total_files = len(tasks)
            self._search.emit(0, 0)
            await asyncio.gather(*tasks)

            if tasks: self._success.emit(1)
            else: self._success.emit(0)


    async def _worker(self, link: str, sem: asyncio.Semaphore) -> None:
        async with sem:
            file: File = File(link=link, progress=self.progress[int], message=self.message[str], file_info=self.file_info[int, int])
            await file.get_file()


    def start_downloading(self) -> None:
        CurrentValues.session = ClientSession(timeout=None, headers={"Connection": "keep-alive"})
        self._downloading = asyncio.run_coroutine_threadsafe(self._get_files(), asyncio.get_event_loop())

    def cancel_downloading(self) -> None:
        if self._downloading:
            asyncio.get_event_loop().call_soon_threadsafe(self._downloading.cancel)
