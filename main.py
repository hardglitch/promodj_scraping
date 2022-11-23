import asyncio
from modules import Base, Data


if __name__ == "__main__":
    music = Base()
    music.download_dir = Data.VALUES["download_dir"]
    music.genre = Data.VALUES["genre"]
    music.form = Data.VALUES["form"]
    music.quantity = Data.VALUES["quantity"]
    music.download = Data.VALUES["download"]
    music.threads = Data.VALUES["threads"]

    asyncio.run(music.get_files())
