import asyncio
from modules.base import Base


if __name__ == "__main__":
    music = Base()
    music.download_dir = f"G:\\_DOWNLOADS\\_MUSIC\\"
    music.genre = "trance"
    music.form = "tracks"
    music.quantity = 10
    music.download = False
    music.threads = 4

    asyncio.run(music.get_files())
