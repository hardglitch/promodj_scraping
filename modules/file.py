from inspect import stack
from pathlib import Path
from time import time

from PyQt6.QtCore import pyqtBoundSignal
from aiofiles import open
from aiohttp import StreamReader

from data.data import CONST
from data.messages import MESSAGES
from modules import db, debug
from modules.shared import CurrentValues
from util import tools


class File:

    __slots__ = "_link", "_name", "_path", "progress", "message", "file_info"

    def __init__(self,
                 link: str,
                 progress: pyqtBoundSignal,
                 message: pyqtBoundSignal,
                 file_info: pyqtBoundSignal
        ):
        self.progress = progress
        self.message = message
        self.file_info = file_info

        if not link:
            debug.log(MESSAGES.Errors.NoLinkToDownload + f" in {stack()[0][3]}")
            self.message.emit(MESSAGES.Errors.NoLinkToDownload)
            return

        self._link: str = link
        self._name: str = str(tools.clear_path(self._link.rsplit("/", 1)[-1]))
        self._path: Path = Path(CurrentValues.download_dir).joinpath(self._name)


    @debug.switch(debug.Switches.IS_GET_FILE)
    async def get_file(self) -> None:
        self._check_path_and_name()
        self.file_info.emit(CurrentValues.total_downloaded_files, CurrentValues.total_files)
        if await self._download_file():
            CurrentValues.total_downloaded_files += 1
            self.file_info.emit(CurrentValues.total_downloaded_files, CurrentValues.total_files)
            if CurrentValues.is_file_history:
                await db.write_file_history(link=self._link, date=int(time()))

# --------------------------------------------------------------------------------------

    def _check_path_and_name(self) -> None:
        if Path(self._path).exists() and not CurrentValues.is_rewrite_files and not CurrentValues.is_file_history:
            ext_time: str = str(time()).replace(".", "")
            ext_pos: int = self._name.rfind(".")
            self._name = self._name[:ext_pos] + "_" + ext_time + self._name[ext_pos:]
            self._path = Path(CurrentValues.download_dir).joinpath(self._name)


    @debug.switch(debug.Switches.IS_DOWNLOAD)
    async def _download_file(self) -> bool:
        try:
            async with CurrentValues.session.get(self._link, timeout=None,
                                                 headers={"Connection": "keep-alive"}) as response:
                if response.status != 200:
                    debug.log(MESSAGES.Errors.SomethingWentWrong + f" in {stack()[0][3]}. {response.status=}")
                    return False
                if await self._write_file(response.content):
                    debug.print_message(f"File save as {self._path}")
                    return True
                else:
                    debug.log(MESSAGES.Errors.UnableToDownloadAFile + f" in {stack()[0][3]}")
                    return False

        except Exception as error:
            debug.log(MESSAGES.Errors.UnableToDownloadAFile + f" in {stack()[0][3]}", error)
            self._gui_exception()
            return False


    @debug.switch(debug.Switches.IS_WRITE_FILE)
    async def _write_file(self, content: StreamReader) -> bool:
        async with open(self._path, "wb") as file:
            debug.print_message(f"Downloading - {self._link}")
            chunk_size: int = 16144
            async for chunk in content.iter_chunked(chunk_size):
                if not chunk: return False
                CurrentValues.total_downloaded += chunk_size
                self._gui_progress()
                await file.write(chunk)
            return True

    @debug.switch(debug.Switches.IS_GUI)
    def _gui_progress(self) -> None:
        if 0 < CurrentValues.total_files < CONST.DefaultValues.file_threshold:
            self.progress.emit(
                round(100 * CurrentValues.total_downloaded / (CurrentValues.total_size * 1.21)))
        elif CurrentValues.total_files >= CONST.DefaultValues.file_threshold:
            self.progress.emit(
                round((100 * CurrentValues.total_downloaded_files / CurrentValues.total_files)))

    @debug.switch(debug.Switches.IS_GUI)
    def _gui_exception(self) -> None:
        self.message.emit(MESSAGES.Errors.UnableToDownloadAFile)
