import asyncio
from modules import Base, Data


if __name__ == "__main__":
    music = Base(Data.VALUES["download_dir"],
                 Data.VALUES["genre"],
                 Data.VALUES["form"],
                 Data.VALUES["quantity"],
                 Data.VALUES["download"],
                 Data.VALUES["threads"])

    asyncio.run(music.get_files())
