from dataclasses import dataclass
from typing import Optional

from aiohttp import ClientSession

from data.data import CONST


@dataclass
class __CurrentValues:

    __slots__ = (
        "__download_dir",
        "__genre",
        "__form",
        "__quantity",
        "__threads",
        "__is_lossless",
        "__is_period",
        "__is_rewrite_files",
        "__is_file_history",
        "__session",
        "__total_files",
        "__total_downloaded_files",
        "__total_downloaded",
        "__total_size"
    )

    __download_dir: str
    __genre: str
    __form: CONST.FORMS
    __quantity: int
    __threads: int
    __is_lossless: bool
    __is_period: bool
    __is_rewrite_files: bool
    __is_file_history: bool
    __session: Optional[ClientSession]
    __total_files: int
    __total_downloaded_files: int
    __total_downloaded: int
    __total_size: int

    def __post_init__(self):
        self.download_dir = self.__download_dir
        self.genre = self.__genre
        self.form = self.__form
        self.quantity = self.__quantity
        self.threads = self.__threads
        self.is_lossless = self.__is_lossless
        self.is_period = self.__is_period
        self.is_rewrite_files = self.__is_rewrite_files
        self.is_file_history = self.__is_file_history
        self.session = self.__session
        self.total_files = self.__total_files
        self.total_downloaded_files = self.__total_downloaded_files
        self.total_downloaded = self.__total_downloaded
        self.total_size = self.__total_size

    @property
    def download_dir(self) -> str:
        return self.__download_dir
    @download_dir.setter
    def download_dir(self, value: str):
        self.__download_dir = value
    @property
    def genre(self) -> str:
        return self.__genre
    @genre.setter
    def genre(self, value: str):
        self.__genre = value
    @property
    def form(self) -> CONST.FORMS:
        return self.__form
    @form.setter
    def form(self, value: CONST.FORMS):
        self.__form = value
    @property
    def quantity(self) -> int:
        return self.__quantity
    @quantity.setter
    def quantity(self, value: int):
        self.__quantity = value
    @property
    def threads(self) -> int:
        return self.__threads
    @threads.setter
    def threads(self, value: int):
        self.__threads = value
    @property
    def is_lossless(self) -> bool:
        return self.__is_lossless
    @is_lossless.setter
    def is_lossless(self, value: bool):
        self.__is_lossless = value
    @property
    def is_period(self) -> bool:
        return self.__is_period
    @is_period.setter
    def is_period(self, value: bool):
        self.__is_period = value
    @property
    def is_rewrite_files(self) -> bool:
        return self.__is_rewrite_files
    @is_rewrite_files.setter
    def is_rewrite_files(self, value: bool):
        self.__is_rewrite_files = value
    @property
    def is_file_history(self) -> bool:
        return self.__is_file_history
    @is_file_history.setter
    def is_file_history(self, value: bool):
        self.__is_file_history = value
    @property
    def session(self) -> Optional[ClientSession]:
        return self.__session
    @session.setter
    def session(self, value: Optional[ClientSession]):
        self.__session = value
    @property
    def total_files(self) -> int:
        return self.__total_files
    @total_files.setter
    def total_files(self, value: int):
        self.__total_files = value
    @property
    def total_downloaded_files(self) -> int:
        return self.__total_downloaded_files
    @total_downloaded_files.setter
    def total_downloaded_files(self, value: int):
        self.__total_downloaded_files = value
    @property
    def total_downloaded(self) -> int:
        return self.__total_downloaded
    @total_downloaded.setter
    def total_downloaded(self, value: int):
        self.__total_downloaded = value
    @property
    def total_size(self) -> int:
        return self.__total_size
    @total_size.setter
    def total_size(self, value: int):
        self.__total_size = value


CurrentValues = __CurrentValues("", "", "", 0, 0, False, False, False, False, None, 0, 0, 0, 0)
