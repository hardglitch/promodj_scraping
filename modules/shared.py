from typing import Optional

from aiohttp import ClientSession

from data.data import CONST


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
        self.__download_dir: str = CONST.DefaultValues.download_dir
        self.__genre: str = CONST.DefaultValues.genre
        self.__form: CONST.DefaultValues.FORMS = CONST.DefaultValues.form
        self.__quantity: int = CONST.DefaultValues.quantity
        self.__threads: int = CONST.DefaultValues.threads
        self.__is_lossless: bool = CONST.DefaultValues.is_lossless
        self.__is_period: bool = CONST.DefaultValues.is_period
        self.__is_rewrite_files: bool = CONST.DefaultValues.is_rewrite_files
        self.__is_file_history: bool = CONST.DefaultValues.is_file_history
        self.__session: Optional[ClientSession] = None
        self.__total_files: int = 0
        self.__total_downloaded_files: int = 0
        self.__total_downloaded: int = 0
        self.__total_size: int = 0


    @property
    def download_dir(self) -> str:
        return self.__download_dir
    @download_dir.setter
    def download_dir(self, value: str) -> None:
        if not isinstance(value, str): raise TypeError
        self.__download_dir = value

    @property
    def genre(self) -> str:
        return self.__genre
    @genre.setter
    def genre(self, value: str) -> None:
        if not isinstance(value, str): raise TypeError
        if value in CONST.DefaultValues.genres: self.__genre = value

    @property
    def form(self) -> CONST.DefaultValues.FORMS:
        return self.__form
    @form.setter
    def form(self, value: CONST.DefaultValues.FORMS) -> None:
        if not isinstance(value, str): raise TypeError
        self.__form = value

    @property
    def quantity(self) -> int:
        return self.__quantity
    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__quantity = value \
            if 0 < value <= abs(CONST.MaxValues.quantity) \
            else abs(CONST.DefaultValues.quantity)

    @property
    def threads(self) -> int:
        return self.__threads
    @threads.setter
    def threads(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__threads = value \
            if 0 < value <= abs(CONST.MaxValues.threads) \
            else abs(CONST.DefaultValues.threads)

    @property
    def is_lossless(self) -> bool:
        return self.__is_lossless
    @is_lossless.setter
    def is_lossless(self, value: bool) -> None:
        if not isinstance(value, bool): raise TypeError
        self.__is_lossless = value

    @property
    def is_period(self) -> bool:
        return self.__is_period
    @is_period.setter
    def is_period(self, value: bool) -> None:
        if not isinstance(value, bool): raise TypeError
        self.__is_period = value

    @property
    def is_rewrite_files(self) -> bool:
        return self.__is_rewrite_files
    @is_rewrite_files.setter
    def is_rewrite_files(self, value: bool) -> None:
        if not isinstance(value, bool): raise TypeError
        self.__is_rewrite_files = value

    @property
    def is_file_history(self) -> bool:
        return self.__is_file_history
    @is_file_history.setter
    def is_file_history(self, value: bool) -> None:
        if not isinstance(value, bool): raise TypeError
        self.__is_file_history = value

    @property
    def session(self) -> Optional[ClientSession]:
        return self.__session
    @session.setter
    def session(self, value: Optional[ClientSession]) -> None:
        if not isinstance(value, Optional[ClientSession]): raise TypeError
        self.__session = value

    @property
    def total_files(self) -> int:
        return self.__total_files
    @total_files.setter
    def total_files(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__total_files = value

    @property
    def total_downloaded_files(self) -> int:
        return self.__total_downloaded_files
    @total_downloaded_files.setter
    def total_downloaded_files(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__total_downloaded_files = value

    @property
    def total_downloaded(self) -> int:
        return self.__total_downloaded
    @total_downloaded.setter
    def total_downloaded(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__total_downloaded = value

    @property
    def total_size(self) -> int:
        return self.__total_size
    @total_size.setter
    def total_size(self, value: int) -> None:
        if not isinstance(value, int): raise TypeError
        self.__total_size = value


CurrentValues = __CurrentValues()
