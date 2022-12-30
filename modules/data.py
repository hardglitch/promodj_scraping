from dataclasses import dataclass


@dataclass()
class Data:

    GENRES = {}

    FORMS = ["mixes", "tracks", "lives"]

    LOSSLESS_FORMATS = [".flac", ".wav", ".aiff"]
    LOSSY_FORMATS = [".mp3"]

    PRINTING: bool = False

    class Values:
        download_dir: str = ""
        genre: str = "trance"
        form: str = "tracks"
        quantity: int = 10
        threads: int = 1
        is_lossless: bool = True
        is_download: bool = True

    class MaxValues:
        quantity: int = 1000
        threads: int = 4