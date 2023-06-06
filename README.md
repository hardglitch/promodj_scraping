**PromoDJ Music Downloader / PromoDJ Scraper**
<br/>
<br/>
<br/>
![1](https://user-images.githubusercontent.com/49201692/223825480-5e86b22a-dcfb-4c3c-bfc1-91249cb16f4c.png)
<br/>
<br/>
***
PromoDJ is the Great site for (electronic) music lovers like me, that allows you to download high quality (electronic) music absolutely free (everything within the law). 
This App will give you the opportunity to download tracks/mixes/lives from this site in a convenient way.
<br/>
<br/>
![2](https://user-images.githubusercontent.com/49201692/223827411-c16e1703-4eb0-46a8-bf1c-3ce0bd5ebb96.png)
<br/>
<br/>
PromoDJ Scraper is completely portable and is distributed in 2 forms: packaged and unpacked.
In the first case, PyInstaller assembles the all used files into a single executable.
It is more convenient to use the App, but Its launch speed may be slower.
The unpacked version solves this problem.
<br/>
<br/>
The user interface has been translated into English, Russian and Ukrainian.

![04](https://github.com/hardglitch/promodj_scraping/assets/49201692/ee5610c9-feed-4099-aeed-27441bced248)


There are also detailed tooltips,

![3](https://github.com/hardglitch/promodj_scraping/assets/49201692/5fd16554-72ef-4d51-b3b1-e3ceffe88e06)

a dark/light theme switcher,

![05](https://github.com/hardglitch/promodj_scraping/assets/49201692/efbfa9c8-26bc-4cd4-925c-f5f918e403c8)

and all the settings you need.

You can download up to 4 files at the same time.
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
