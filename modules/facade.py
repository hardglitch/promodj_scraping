from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import QMainWindow
from aiohttp import ClientSession

from modules.data import Data


class ManagerInit(QMainWindow):
    def __init__(self,
                 download_dir: Path = Path(Data.DefaultValues.download_dir),
                 genre: str = Data.DefaultValues.genre,
                 form: str = Data.DefaultValues.form,
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

    download_dir: str
    genre: str
    form: str
    quantity: int
    threads: int
    is_lossless: bool
    is_period: bool
    is_rewrite_files: bool
    is_file_history: bool
    session: Optional[ClientSession]

    total_files: int
    total_downloaded_files: int
    total_downloaded: int
    total_size: int
