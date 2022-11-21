from . import utils
from .data import Data
from bs4 import BeautifulSoup, ResultSet
from typing import Any
import asyncio
import aiohttp


class Base:

    def __int__(self) -> None:
        self.download_dir: str = "music"
        self.genre: str = "trance"
        self.form: str = "tracks"
        self.quantity: int = 10
        self.download: bool = True
        self.threads: int = 4

    def limiter(self, param: Any) -> Any:
        param = param.lower() if type(param) is str else param
        if param == self.form.lower() and param in Data.FORMS \
                or param == self.genre and param in Data.GENRES:
            return param
        if param == self.quantity:
            param = param if 0 < param <= 1000 else 10
            return param
        if param == self.threads:
            param = param if 0 < param <= 8 else 4
            return param
        print(param)
        print("Something went wrong")
        exit()

    def get_filtered_links(self, links_massive: ResultSet = None) -> list:
        if links_massive is None:
            print("No Links to filtering")
            exit()

        filtered_links = {}
        for link in links_massive:
            for frmt in Data.FORMATS:
                if link.has_attr("href") and link["href"].find(frmt) > -1:
                    filtered_links[link["href"]] = 1  # deduplication
        return list(filtered_links.keys())

    async def get_all_links(self, session: aiohttp.ClientSession = None) -> list:
        if session is None:
            print("Unable to download")
            exit()

        page: int = 1
        found_links: list = []
        quantity = self.limiter(self.quantity)
        genre = self.limiter(self.genre)
        form = self.limiter(self.form)

        while len(found_links) < quantity:
            link = f"https://promodj.com/{form}/{genre}?bitrate=lossless&page={page}"
            async with session.get(link) as response:
                if response.status == 404: break
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                found_links += self.get_filtered_links(links)
                page += 1
        tmp = {}
        for n in found_links: tmp[n] = 1
        return list(tmp)[:quantity]

    async def get_file_name_from_link(self, link: str = None) -> str:
        if link is None:
            print("No Link to extract a name")
            return ""

        decode_simbols = {"%20": " ", "%28": "(", "%29": ")", "%26": "&", "%23": "#"}

        filename: str = link.split("/")[-1]

        for i in decode_simbols:
            filename = filename.replace(i, decode_simbols[i])

        index = 0
        while index != -1:
            index = filename.find(fr"%")
            smb = filename[index:index + 3]
            filename = filename.replace(fr"{smb:2}", "")

        return filename.strip()

    async def get_file_by_link(self, session: aiohttp.ClientSession = None, link: str = None):
        if link is None:
            print("No Link to download")
            exit()
        if session is None:
            print("Unable to connect")
            exit()

        filename = await self.get_file_name_from_link(link)
        if self.download:
            async with session.get(link) as response:
                if response.status != 200:
                    print("Something went wrong")
                    return
                async with open(self.download_dir + filename, "wb") as file:
                    print(f"Downloading {filename}...")
                    await file.write(response.content)

        print(f"File save as {self.download_dir + filename}")

    @utils.async_timer()
    async def get_files(self):
        async with aiohttp.ClientSession() as session:
            links_future = asyncio.as_completed([self.get_all_links(session)])
            for links in links_future:
                for link in await links:
                    task = asyncio.create_task(self.get_file_by_link(session, link))
                    try:
                        await asyncio.wait_for(task, timeout=5)
                    except asyncio.exceptions.TimeoutError:
                        print("Something went wrong")
