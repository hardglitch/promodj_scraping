from dataclasses import dataclass

@dataclass()
class Data:

    FORMS = ("mixes", "tracks", "lives")

    LOSSLESS_FORMATS = (".flac", ".wav", ".aiff")
    LOSSY_FORMATS = [".mp3"]
    DB_NAME = "history.db"

    PRINTING: bool = False   # for console output

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
        is_download: bool = True   # for testing

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
