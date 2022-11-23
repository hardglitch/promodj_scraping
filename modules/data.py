from dataclasses import dataclass


@dataclass()
class Data:

    GENRES = ["trance", "uplifting_trance", "techno", "dnb", "deep_house", "2_step", "liquid_funk", "neurofunk",
              "jungle"]

    FORMS = ["mixes", "tracks", "lives"]

    FORMATS = [".flac", ".wav", ".aiff"]

    VALUES = {"download_dir": f"G:\\_DOWNLOADS\\_MUSIC\\",
              "genre": "trance",
              "form": "tracks",
              "quantity": 10,
              "download": True,
              "threads": 4,
              }

    MAX_VALUES = {"quantity": 1000,
                  "threads": 8,
                  }

