from . import utils
from .data import Data
from bs4 import BeautifulSoup, ResultSet
from typing import Any
import asyncio
import aiohttp
import aiofiles


class Base:

    def __init__(self,
                 download_dir: str = "music",
                 genre: str = "trance",
                 form: str = "tracks",
                 quantity: int = 10,
                 download: bool = True,
                 threads: int = 4) -> None:

        self.download_dir: str = download_dir
        self.genre: str = self.limiter(genre)
        self.form: str = self.limiter(form)
        self.quantity: int = self.limiter(quantity)
        self.download: bool = download
        self.threads: int = self.limiter(threads)

    def limiter(self, param: Any) -> Any:
        param = param.lower() if type(param) is str else param
        if param == self.form.lower() and param in Data.FORMS \
                or param == self.genre and param in Data.GENRES:
            return param
        if param == self.quantity:
            param = param if param <= abs(Data.MAX_VALUES["quantity"]) else Data.MAX_VALUES["quantity"]
            return param
        if param == self.threads:
            param = param if param <= abs(Data.MAX_VALUES["threads"]) else Data.MAX_VALUES["threads"]
            return param
        print("No suitable parameter")
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
                    print("Something went wrong 2")
                    return
                async with aiofiles.open(self.download_dir + filename, "wb") as file:
                    print(f"Downloading {filename}...")
                    async for data in response.content.iter_chunked(1024):
                        await file.write(data)
        print(f"File save as {self.download_dir + filename}")

    async def dl_threads_limiter(self, sem: asyncio.Semaphore = None,
                                 session: aiohttp.ClientSession = None, link: str = None):
        async with sem:
            return await self.get_file_by_link(session, link)

    @utils.async_timer()
    async def get_files(self):
        async with aiohttp.ClientSession() as session:
            links_future = asyncio.as_completed([self.get_all_links(session)])
            sem = asyncio.Semaphore(self.limiter(self.threads))
            tasks = []
            for links in links_future:
                for link in await links:
                    tasks.append(asyncio.ensure_future(self.dl_threads_limiter(sem, session, link)))
            await asyncio.gather(*tasks)
