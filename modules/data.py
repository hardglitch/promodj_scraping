from dataclasses import dataclass

@dataclass()
class Data:

    FORMS = ("mixes", "tracks", "lives")

    LOSSLESS_FORMATS = (".flac", ".wav", ".aiff", ".alac", ".tta", ".ape", ".wv")
    LOSSY_FORMATS = (".mp3",)
    DB_NAME = "history.db"

    class DefaultValues:
        download_dir = "Downloaded Music"
        genre = "Trance"
        form = "tracks"
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
        DownloadDirectory = "DownloadDirectory"
        Genre = "Genre"
        Form = "Form"
        Lossless = "Lossless"
        Period = "Period"
        Quantity = "Quantity"
        Threads = "Threads"
        RewriteFiles = "RewriteFiles"
        FileHistory = "FileHistory"
        LastDownload = "LastDownload"

    class Inscriptions:
        PromoDJMusicDownloader = "PromoDJ Music Downloader"
        PromoDJMusicDownloaderExtended = PromoDJMusicDownloader + " --- Last download was _ days ago"
        Files = "files"
        Period = "Period"
        Lossless = "Lossless"
        FileHistory = "File History"
        RewriteFiles = "Rewrite Files"
        Threads = "threads"
        SaveTo = "Save to"
        Download = "Download"
        Exit = "Exit"
        Cancel = "Cancel"
        LastDays = "last days"
