from inspect import stack
from pathlib import Path
from time import time

from PyQt6.QtCore import pyqtSignal
from aiofiles import open

from modules import db, debug
from modules.data import Data
from modules.facade import CurrentValues
from modules.messages import Messages


class File:
    def __init__(self,
                 link: str,
                 progress: pyqtSignal(int),
                 message: pyqtSignal(str),
                 file_info: pyqtSignal(int, int),
        ):
        self.progress = progress
        self.message = message
        self.file_info = file_info

        if not link:
            debug.log(Messages.Errors.NoLinkToDownload)
            self.message[str].emit(Messages.Errors.NoLinkToDownload)
            return

        self._link: str = link
        self._name: str = self._link.rsplit("/", 1)[-1]
        self._path: Path = Path(CurrentValues.download_dir).joinpath(self._name)
        assert isinstance(self._link, str)
        assert isinstance(self._name, str)
        assert isinstance(self._path, Path)


    def _check_path_and_name(self):
        if Path(self._path).exists() and not CurrentValues.is_rewrite_files and not CurrentValues.is_file_history:
            ext_time: str = str(time()).replace(".", "")
            ext_pos: int = self._name.rfind(".")
            self._name = self._name[:ext_pos] + "_" + ext_time + self._name[ext_pos:]
            self._path: Path = Path(CurrentValues.download_dir).joinpath(self._name)

    async def get_file(self):
        self._check_path_and_name()
        self.file_info[int, int].emit(CurrentValues.total_downloaded_files, CurrentValues.total_files)
        if await self._download_file():
            CurrentValues.total_downloaded_files += 1
            self.file_info[int, int].emit(CurrentValues.total_downloaded_files, CurrentValues.total_files)
            if CurrentValues.is_file_history:
                await db.write_file_history(link=self._link, date=int(time()))


    # @debug.is_download()
    async def _download_file(self) -> bool:
        try:
            async with CurrentValues.session.get(self._link, timeout=None) as response:
                if response.status != 200:
                    debug.log(Messages.Errors.SomethingWentWrong + f" in {stack()[0][3]}. {response.status=}")
                    return False

                async with open(self._path, "wb") as file:
                    debug.print_message(f"Downloading - {self._link}")
                    chunk_size: int = 16144
                    async for chunk in response.content.iter_chunked(chunk_size):
                        if not chunk: break
                        CurrentValues.total_downloaded += chunk_size
                        if 0 < CurrentValues.total_files < Data.DefaultValues.file_threshold:
                            self.progress[int].emit(
                                round(100 * CurrentValues.total_downloaded / (CurrentValues.total_size * 1.21)))
                        elif CurrentValues.total_files >= Data.DefaultValues.file_threshold:
                            self.progress[int].emit(
                                round((100 * CurrentValues.total_downloaded_files / CurrentValues.total_files)))
                        else: pass
                        await file.write(chunk)

                    debug.print_message(f"File save as {self._path}")
                    return True

        except Exception as error:
            print(error)
            debug.log(Messages.Errors.UnableToDownloadAFile + f" in {stack()[0][3]}", error)
            self.message[str].emit(Messages.Errors.UnableToDownloadAFile)
            return False
