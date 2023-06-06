**PromoDJ Music Downloader / PromoDJ Scraper**
<br/>
<br/>
<br/>
![1](https://user-images.githubusercontent.com/49201692/223825480-5e86b22a-dcfb-4c3c-bfc1-91249cb16f4c.png)
<br/>
<br/>
***
[PromoDJ.com](https://promodj.com) is the Great site for (electronic) music lovers like me, that allows you to download high quality (electronic) music absolutely free (everything within the law). 
This App will give you the opportunity to download tracks/mixes/lives from this site in a convenient way.

PromoDJ Scraper is completely portable and is distributed in 2 forms: packaged and unpacked.
In the first case, PyInstaller assembles the all used files into a single executable.
It is more convenient to use the App, but Its launch speed may be slower.
The unpacked version solves this problem.

The user interface has been translated into English, Russian and Ukrainian.
***
<br/>

![2](https://user-images.githubusercontent.com/49201692/223827411-c16e1703-4eb0-46a8-bf1c-3ce0bd5ebb96.png)
<br/>
<br/>

***
Stack:
<pre>
- asyncio
- PyQt6 + qasync (GUI)
- aiofiles (IO)
- aiosqlite (SQLite)
- aiohttp (Web)
- beautifulsoup4 + lxml (Parsing)

- mypy
- pyright
- bandit

- pytest + pytest-asyncio + pytest-xdist
- allure

- pyinstaller (Package Builder)
</pre>
