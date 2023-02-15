import asyncio
from inspect import stack

from PyQt6.QtCore import pyqtSignal

from modules import debug
from modules.facade import CurrentValues
from modules.messages import Messages


class Task:

    search = pyqtSignal(int, int)

    def __init__(self,
                 micro_link: str,
                 search: pyqtSignal(str)
        ):
        self._micro_link = micro_link
        self.search = search

    async def micro_task(self, counter: int = 0):
        async with CurrentValues.session.get(self._micro_link, timeout=None) as response:
            if response.status != 200:
                return debug.log(Messages.Errors.SomethingWentWrong
                                 + f" in {stack()[0][3]}. {response.status=}")
            CurrentValues.total_size += response.content_length if response.content_length else 0
            self.search[int, int].emit(counter % 5, 2)

class Pool:

    _counter: int = 0
    def __init__(self, threads: int = 4, interval: float = 0.1):
        self.threads: int = threads
        self.interval: float = interval
        self._queue = asyncio.Queue()

    async def _worker(self, task: Task):
        self._counter += 1
        await task.micro_task(self._counter)
        self._queue.task_done()

    async def put(self, task: Task):
        await self._queue.put(task)

    async def join(self):
        await self._queue.join()

    async def start(self):
        while not self._queue.empty():
            async with asyncio.Semaphore(self.threads):
                task = await self._queue.get()
                asyncio.create_task(self._worker(task))
                await asyncio.sleep(self.interval)
