from modules.data import Data
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class Base:

    def __int__(self, download_dir: str = None, genre: str = "trance", form: str = "tracks",
                quantity: int = 10, download: bool = True, threads: int = 4):
        self.download_dir: str = download_dir.lower()
        self.genre: str = genre.lower() if genre.lower() in Data.GENRES else "trance"
        self.form: str = form if form in Data.FORMS else "tracks"
        self.quantity: int = quantity if 1000 < quantity > 0 else 10
        self.download: bool = download
        self.threads: int = threads if 8 < threads > 0 else 4

    def get_filtered_links(self, links_massive) -> list:
        filtered_links = {}
        for link in links_massive:
            for frmt in Data.FORMATS:
                if link.has_attr("href") and link["href"].find(frmt) > -1:
                    filtered_links[link["href"]] = 1                            # deduplication
        return list(filtered_links.keys())

    async def get_all_links(self, session: aiohttp.ClientSession = None) -> list:
        page: int = 1
        found_links: list = []
        while len(found_links) < self.quantity:
            link = f"https://promodj.com/{self.form}/{self.genre}?bitrate=lossless&page={page}"
            async with session.get(link) as response:
                if response.status == 404: break
                links = BeautifulSoup(await response.read(), features="html.parser").findAll("a")
                found_links += self.get_filtered_links(links)
                page += 1
        tmp = {}
        for n in found_links: tmp[n] = 1
        return list(tmp)[:self.quantity]

    def get_file_name_from_link(self, link: str = None) -> str:
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
        filename = self.get_file_name_from_link(link)
        if self.download:
            async with session.get(link) as response:
                if response.status != 200:
                    print("Something went wrong")
                    return
                async with open(self.download_dir + filename, "wb") as file:
                    print(f"Downloading {filename}...")
                    await file.write(response.content)

        print(f"File save as {self.download_dir + filename}")

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
