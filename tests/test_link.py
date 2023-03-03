from typing import Set

import aiofiles
import pytest
from PyQt6.QtCore import pyqtSignal
from bs4 import BeautifulSoup, ResultSet, SoupStrainer

from modules import debug
from modules.link import Link
from modules.shared import CurrentValues

progress = pyqtSignal(int)
success = pyqtSignal(int)
search = pyqtSignal(int, int)
message = pyqtSignal(str)
file_info = pyqtSignal(int, int)

CurrentValues.is_file_history = False
debug.Switches.IS_GUI = False
link = Link(message=progress[int], success=success[int], search=search[int, int])


@pytest.mark.asyncio
async def test_filtered_found_links_positive():
    found_links = {"1.flac", "2.flac", "2.wav","1.wav"}
    assert isinstance(found_links, Set)
    assert all(map(lambda x: True if type(x)==str else False, found_links))
    assert await link._filtered_found_links(found_links) in [
        {"1.flac", "2.flac"}, {"1.wav", "2.wav"}, {"1.flac", "2.wav"}, {"1.wav", "2.flac"}]

@pytest.mark.asyncio
async def test_filtered_found_links_negative_1():
    found_links = set()
    assert await link._filtered_found_links(found_links) == set()

@pytest.mark.asyncio
async def test_filtered_found_links_negative_2():
    found_links = [1,2,3]
    assert await link._filtered_found_links(found_links) == set()


async def setup_resultset() -> ResultSet:
    async with aiofiles.open("testpage.html", "r", encoding="utf-8") as file: test_page = await file.read()
    return BeautifulSoup(test_page, "lxml", parse_only=SoupStrainer("a")).findAll(href=True)

@pytest.mark.asyncio
async def test_get_filtered_links_lossless():
    CurrentValues.is_lossless = True
    assert link._get_filtered_links(await setup_resultset()) == {
        fr"https://promodj.com/source/some1.flac",
        fr"https://promodj.com/source/some2.wav",
        fr"https://promodj.com/source/some22.aiff",
    }

@pytest.mark.asyncio
async def test_get_filtered_links_lossy():
    CurrentValues.is_lossless = True
    assert link._get_filtered_links(await setup_resultset()) == {
        fr"https://promodj.com/source/some3.mp3"
    }

@pytest.mark.asyncio
async def test_get_filtered_links_lossy():
    link_massive = ResultSet(SoupStrainer())
    assert isinstance(link_massive, ResultSet)
    assert link._get_filtered_links(link_massive) == set()
