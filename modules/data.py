from dataclasses import dataclass
from typing import Literal, Tuple


@dataclass(frozen=True)
class Data:

    FORMS = Literal["mixes", "tracks", "lives"]
    LOSSLESS_UNCOMPRESSED_FORMATS: Tuple[str] = (".wav", ".aiff")
    LOSSLESS_COMPRESSED_FORMATS: Tuple[str] = (".flac", ".alac", ".tta", ".ape", ".wv")
    LOSSY_FORMATS: Tuple[str] = (".mp3",)
    DB_NAME: str = "history.db"

    @dataclass(frozen=True)
    class DefaultValues:
        download_dir: str = "Downloaded Music"
        genre: str = "Trance"
        form: str = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_period: bool = False
        is_rewrite_files: bool = False
        is_file_history: bool = True
        file_threshold: int = 50

    @dataclass(frozen=True)
    class MaxValues:
        quantity: int = 1000
        threads: int = 4

    @dataclass(frozen=True)
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

    @dataclass(frozen=True)
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

