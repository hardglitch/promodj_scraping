from dataclasses import dataclass
from typing import AnyStr

@dataclass()
class Data:

    FORMS = ("mixes", "tracks", "lives")

    LOSSLESS_FORMATS = (".flac", ".wav", ".aiff")
    LOSSY_FORMATS = [".mp3"]
    DB_NAME = "history.db"

    PRINTING: bool = False   # for testing or console output

    class DefaultValues:
        download_dir: AnyStr = "Downloaded Music"
        genre: AnyStr = "Trance"
        form: AnyStr = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_period: bool = False
        is_rewrite_files: bool = True
        is_file_history: bool = True
        is_download: bool = True   # for testing

    class MaxValues:
        quantity: int = 1000
        threads: int = 4

    class Parameters:
        DownloadDirectory: AnyStr = "DownloadDirectory"
        Genre: AnyStr = "Genre"
        Form: AnyStr = "Form"
        Lossless: AnyStr = "Lossless"
        Period: AnyStr = "Period"
        Quantity: AnyStr = "Quantity"
        Threads: AnyStr = "Threads"
        RewriteFiles: AnyStr = "RewriteFiles"
        FileHistory: AnyStr = "FileHistory"
        LastDownload: AnyStr = "LastDownload"

    class Inscriptions:
        PromoDJMusicDownloader: AnyStr = "PromoDJ Music Downloader"
        PromoDJMusicDownloaderExtended: AnyStr = PromoDJMusicDownloader + " --- Last download was _ days ago"
        Files: AnyStr = "files"
        Period: AnyStr = "Period"
        Lossless: AnyStr = "Lossless"
        FileHistory: AnyStr = "File History"
        RewriteFiles: AnyStr = "Rewrite Files"
        Threads: AnyStr = "threads"
        SaveTo: AnyStr = "Save to"
        Download: AnyStr = "Download"
        Exit: AnyStr = "Exit"
        Cancel: AnyStr = "Cancel"
        LastDays: AnyStr = "last days"
