import asyncio
from concurrent.futures import Future
from typing import Optional, Set

from PyQt6.QtCore import pyqtSignal
from aiohttp import ClientSession

from modules import db
from modules.facade import CurrentValues, ManagerInit
from modules.file import File
from modules.link import Link


class Manager(ManagerInit):

    progress = pyqtSignal(int)
    success = pyqtSignal(int)
    search = pyqtSignal(int, int)
    message = pyqtSignal(str)
    file_info = pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._downloading: Optional[Future] = None

    async def _get_files(self):
        async with CurrentValues.session:
            if CurrentValues.is_file_history: await db.create_history_db()

            link: Link = Link(message=self.progress, success=self.success, search=self.search)
            all_links: Set[str] = await link.get_all_links()
            if not all_links: return self.success[int].emit(0)
            assert isinstance(all_links, Set)
            assert all(map(lambda x: True if type(x)==str else False, all_links))

            tasks = []
            sem = asyncio.Semaphore(CurrentValues.threads)
            [tasks.append(asyncio.ensure_future(self._worker(_link, sem))) for _link in all_links]
            CurrentValues.total_files = len(tasks)
            self.search[int, int].emit(0, 0)
            await asyncio.gather(*tasks)

            if tasks: self.success[int].emit(1)
            else: self.success[int].emit(0)

    async def _worker(self, link: str, sem: asyncio.Semaphore):
        async with sem:
            file: File = File(link=link, progress=self.progress, message=self.message, file_info=self.file_info)
            await file.get_file()

    def start_downloading(self):
        CurrentValues.session = ClientSession(timeout=None, headers={"Connection": "keep-alive"})
        self._downloading = asyncio.run_coroutine_threadsafe(self._get_files(), asyncio.get_event_loop())

    def cancel_downloading(self):
        if self._downloading:
            asyncio.get_event_loop().call_soon_threadsafe(self._downloading.cancel)
