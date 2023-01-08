from dataclasses import dataclass


@dataclass()
class Data:

    FORMS = ["mixes", "tracks", "lives"]

    LOSSLESS_FORMATS = [".flac", ".wav", ".aiff"]
    LOSSY_FORMATS = [".mp3"]

    PRINTING: bool = False    # for testing or console output

    class Values:                  # default values
        download_dir: str = "Downloaded Music"
        genre: str = "Trance"
        form: str = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_period: bool = False
        is_download: bool = True   # for testing

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
