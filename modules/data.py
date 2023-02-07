from dataclasses import dataclass
from typing import Tuple

@dataclass()
class Data:

    FORMS: Tuple[str] = ("mixes", "tracks", "lives")

    LOSSLESS_FORMATS: Tuple[str] = (".flac", ".wav", ".aiff", ".alac", ".tta", ".ape", ".wv")
    LOSSY_FORMATS: Tuple[str] = (".mp3",)
    DB_NAME: str = "history.db"

    class DefaultValues:
        download_dir: str = "Downloaded Music"
        genre: str = "Trance"
        form: str = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_period: bool = False
        is_rewrite_files: bool = True
        is_file_history: bool = True

    class MaxValues:
        quantity: int = 1000
        threads: int = 4

    class Parameters:
        DownloadDirectory: str = "DownloadDirectory"
        Genre: str = "Genre"
        Form: str = "Form"
        Lossless: str = "Lossless"
        Period: str = "Period"
        Quantity: str = "Quantity"
        Threads: str = "Threads"
        RewriteFiles: str = "RewriteFiles"
        FileHistory: str = "FileHistory"
        LastDownload: str = "LastDownload"

    class Inscriptions:
        PromoDJMusicDownloader: str = "PromoDJ Music Downloader"
        PromoDJMusicDownloaderExtended: str = PromoDJMusicDownloader + " --- Last download was _ days ago"
        Files: str = "files"
        Period: str = "Period"
        Lossless: str = "Lossless"
        FileHistory: str = "File History"
        RewriteFiles: str = "Rewrite Files"
        Threads: str = "threads"
        SaveTo: str = "Save to"
        Download: str = "Download"
        Exit: str = "Exit"
        Cancel: str = "Cancel"
        LastDays: str = "last days"
