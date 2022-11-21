import asyncio
from modules import Base


if __name__ == "__main__":
    # music = Base(f"G:\\_DOWNLOADS\\_MUSIC\\", "trance", "tracks", 10, False, 10)
    music = Base()
    music.download_dir = f"G:\\_DOWNLOADS\\_MUSIC\\"
    music.genre = "trance"
    music.form = "mixes"
    music.quantity = 10
    music.download = False
    music.threads = 8

    asyncio.run(music.get_files())
