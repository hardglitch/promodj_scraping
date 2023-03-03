from pathlib import Path
from typing import Set

import pytest

from data.data import CONST
from modules import db
from util import tools


@pytest.mark.asyncio
async def test_db():
    try: Path(CONST.DB_NAME).unlink()
    except: pass

    await db.create_history_db()
    assert Path(CONST.DB_NAME).exists()

    link = "test link"
    date = 1234567890
    assert isinstance(link, str)
    assert isinstance(date, int)
    await db.write_file_history(link, date)

    assert not await db.filter_by_history({link})

    found_links = {f"test link{n}" for n in range(10)}
    assert isinstance(found_links, Set)
    assert all(map(lambda x: True if type(x)==str else False, found_links))

    filtered_links = await db.filter_by_history(found_links)
    assert filtered_links == found_links

    Path(CONST.DB_NAME).unlink()


@pytest.mark.asyncio
async def test_write_file_history_bruteforce():
    assert await tools.fuzzer(db.write_file_history)

@pytest.mark.asyncio
async def test_filter_by_history_bruteforce():
    assert await tools.fuzzer(db.filter_by_history)
