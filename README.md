**PromoDJ Music Downloader / PromoDJ Scraper**

![1](https://user-images.githubusercontent.com/49201692/220620326-60fff0c1-a6cb-460e-a788-f86c69b52364.png)

[PromoDJ.com](https://promodj.com) is The Great Site for (electronic) music lovers like me.

This App will give you the opportunity to download tracks/mixes/lives from this site in a convenient way.

PromoDJ Scraper is completely portable. 
It distributed in 2 forms: packed and unpacked.

Packed - pyinstaller assembles all used files in one executable file.
It is more convenient to use the App, but Its launch speed may be slower.

The unpacked version solves this problem.

-------------------------------------------
Stack:
- asyncio
- PyQt6 + qasync (GUI)
- aiofiles (IO)
- aiosqlite (SQLite)
- aiohttp (Web)
- beautifulsoup4 + lxml (Parsing)


- mypy
- pyright
- bandit


- pytest
- allure


- pyinstaller


In test mode
- ruff (fastest Linter)
- Docker (to build the Linux version of the App)