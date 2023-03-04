from inspect import stack
from platform import system
from typing import Optional, get_args

from aiohttp import ClientSession

from data.data import CONST, Data
from modules import debug
from util import tools


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

    def __init__(self) -> None:
        self.download_dir = CONST.DefaultValues.download_dir
        self.genre = CONST.DefaultValues.genre
        self.form = CONST.DefaultValues.form
        self.quantity = CONST.DefaultValues.quantity
        self.threads = CONST.DefaultValues.threads
        self.is_lossless = CONST.DefaultValues.is_lossless
        self.is_period = CONST.DefaultValues.is_period
        self.is_rewrite_files = CONST.DefaultValues.is_rewrite_files
        self.is_file_history = CONST.DefaultValues.is_file_history
        self.session = None
        self.total_files = 0
        self.total_downloaded_files = 0
        self.total_downloaded = 0
        self.total_size = 0


    @property
    def download_dir(self) -> str:
        return self.__download_dir

    @download_dir.setter
    def download_dir(self, value: str) -> None:
        value = tools.clear_path(value)
        if value != Data.DefaultValues.download_dir and system() == "Windows":
            value = tools.insert_string(value, ":", 1)
        if not isinstance(value, str) or not value:
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__download_dir = value


    @property
    def genre(self) -> str:
        return self.__genre

    @genre.setter
    def genre(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        if value in CONST.DefaultValues.genres: self.__genre = value


    @property
    def form(self) -> CONST.DefaultValues.FORMS:
        return self.__form

    @form.setter
    def form(self, value: CONST.DefaultValues.FORMS) -> None:
        if not isinstance(value, str):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        if value in get_args(CONST.DefaultValues.FORMS): self.__form = value


    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__quantity = CONST.MaxValues.quantity if value > CONST.MaxValues.quantity else 0 if value <= 0 else value


    @property
    def threads(self) -> int:
        return self.__threads

    @threads.setter
    def threads(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__threads = CONST.MaxValues.threads if value >= CONST.MaxValues.threads else 1 if value <= 1 else value


    @property
    def is_lossless(self) -> bool:
        return self.__is_lossless

    @is_lossless.setter
    def is_lossless(self, value: bool) -> None:
        if not isinstance(value, bool):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__is_lossless = value


    @property
    def is_period(self) -> bool:
        return self.__is_period

    @is_period.setter
    def is_period(self, value: bool) -> None:
        if not isinstance(value, bool):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__is_period = value


    @property
    def is_rewrite_files(self) -> bool:
        return self.__is_rewrite_files

    @is_rewrite_files.setter
    def is_rewrite_files(self, value: bool) -> None:
        if not isinstance(value, bool):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__is_rewrite_files = value


    @property
    def is_file_history(self) -> bool:
        return self.__is_file_history

    @is_file_history.setter
    def is_file_history(self, value: bool) -> None:
        if not isinstance(value, bool):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__is_file_history = value


    @property
    def session(self) -> Optional[ClientSession]:
        return self.__session

    @session.setter
    def session(self, value: Optional[ClientSession]) -> None:
        if not isinstance(value, ClientSession | None):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__session = value


    @property
    def total_files(self) -> int:
        return self.__total_files

    @total_files.setter
    def total_files(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__total_files = CONST.MaxValues.quantity if value >= CONST.MaxValues.quantity else 0 if value <= 0 else value


    @property
    def total_downloaded_files(self) -> int:
        return self.__total_downloaded_files

    @total_downloaded_files.setter
    def total_downloaded_files(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        self.__total_downloaded_files = CONST.MaxValues.quantity if value >= CONST.MaxValues.quantity else 0 if value <= 0 else value


    @property
    def total_downloaded(self) -> int:
        return self.__total_downloaded

    @total_downloaded.setter
    def total_downloaded(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        if value >= 0: self.__total_downloaded = value
        else:
            self.__total_downloaded = 0
            debug.log(f"ValueError in {stack()[0][3]}")


    @property
    def total_size(self) -> int:
        return self.__total_size

    @total_size.setter
    def total_size(self, value: int) -> None:
        if not isinstance(value, int):
            debug.log(f"TypeError in {stack()[0][3]}")
            raise TypeError
        if value >= 0: self.__total_size = value
        else:
            self.__total_size = 0
            debug.log(f"ValueError in {stack()[0][3]}")


CurrentValues = __CurrentValues()
