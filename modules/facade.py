from dataclasses import dataclass
from typing import Optional

from PyQt6.QtWidgets import QMainWindow
from aiohttp import ClientSession

from modules.data import Data


class ManagerInit(QMainWindow):
    def __init__(self,
                 download_dir: str = Data.DefaultValues.download_dir,
                 genre: str = Data.DefaultValues.genre,
                 form: Data.FORMS = Data.DefaultValues.form,
                 is_lossless: bool = Data.DefaultValues.is_lossless,
                 quantity: int = Data.DefaultValues.quantity,
                 is_period: bool = Data.DefaultValues.is_period,
                 threads: int = Data.DefaultValues.threads,
                 is_rewrite_files: bool = Data.DefaultValues.is_rewrite_files,
                 is_file_history: bool = Data.DefaultValues.is_file_history,
        ):

        super().__init__()
        CurrentValues.download_dir = download_dir
        CurrentValues.genre = genre
        CurrentValues.form = form
        CurrentValues.is_lossless = is_lossless
        CurrentValues.quantity = quantity \
            if 0 < quantity <= abs(Data.MaxValues.quantity) \
            else abs(Data.DefaultValues.quantity)
        CurrentValues.is_period = is_period
        CurrentValues.threads = threads \
            if 0 < threads <= abs(Data.MaxValues.threads) \
            else abs(Data.DefaultValues.threads)
        CurrentValues.is_rewrite_files = is_rewrite_files
        CurrentValues.is_file_history = is_file_history

        CurrentValues.session = None

        CurrentValues.total_files = 0
        CurrentValues.total_downloaded_files = 0
        CurrentValues.total_downloaded = 0
        CurrentValues.total_size = 0


@dataclass
class CurrentValues:

    _download_dir: str
    _genre: str
    _form: Data.FORMS
    _quantity: int
    _threads: int
    _is_lossless: bool
    _is_period: bool
    _is_rewrite_files: bool
    _is_file_history: bool
    _session: Optional[ClientSession]
    _total_files: int
    _total_downloaded_files: int
    _total_downloaded: int
    _total_size: int

    def __post_init__(self):
        self.download_dir = self._download_dir
        self.genre = self._genre
        self.form = self._form
        self.quantity = self._quantity
        self.threads = self._threads
        self.is_lossless = self._is_lossless
        self.is_period = self._is_period
        self.is_rewrite_files = self._is_rewrite_files
        self.is_file_history = self._is_file_history
        self.session = self._session
        self.total_files = self._total_files
        self.total_downloaded_files = self._total_downloaded_files
        self.total_downloaded = self._total_downloaded
        self.total_size = self._total_size

    @property
    def download_dir(self) -> str:
        return self._download_dir
    @download_dir.setter
    def download_dir(self, value: str):
        self._download_dir = value
    @property
    def genre(self) -> str:
        return self._genre
    @genre.setter
    def genre(self, value: str):
        self._genre = value
    @property
    def form(self) -> Data.FORMS:
        return self._form
    @form.setter
    def form(self, value: Data.FORMS):
        self._form = value
    @property
    def quantity(self) -> int:
        return self._quantity
    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value
    @property
    def threads(self) -> int:
        return self._threads
    @threads.setter
    def threads(self, value: int):
        self._threads = value
    @property
    def is_lossless(self) -> bool:
        return self._is_lossless
    @is_lossless.setter
    def is_lossless(self, value: bool):
        self._is_lossless = value
    @property
    def is_period(self) -> bool:
        return self._is_period
    @is_period.setter
    def is_period(self, value: bool):
        self._is_period = value
    @property
    def is_rewrite_files(self) -> bool:
        return self._is_rewrite_files
    @is_rewrite_files.setter
    def is_rewrite_files(self, value: bool):
        self._is_rewrite_files = value
    @property
    def is_file_history(self) -> bool:
        return self._is_file_history
    @is_file_history.setter
    def is_file_history(self, value: bool):
        self._is_file_history = value
    @property
    def session(self) -> Optional[ClientSession]:
        return self._session
    @session.setter
    def session(self, value: Optional[ClientSession]):
        self._session = value
    @property
    def total_files(self) -> int:
        return self._total_files
    @total_files.setter
    def total_files(self, value: int):
        self._total_files = value
    @property
    def total_downloaded_files(self) -> int:
        return self._total_downloaded_files
    @total_downloaded_files.setter
    def total_downloaded_files(self, value: int):
        self._total_downloaded_files = value
    @property
    def total_downloaded(self) -> int:
        return self._total_downloaded
    @total_downloaded.setter
    def total_downloaded(self, value: int):
        self._total_downloaded = value
    @property
    def total_size(self) -> int:
        return self._total_size
    @total_size.setter
    def total_size(self, value: int):
        self._total_size = value
