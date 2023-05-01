from pathlib import Path
from typing import Set
import allure
from data.data import CONST
from modules import db, debug
from util import tools


@allure.epic("Database transactions")
class TestDB:

    @allure.description("Create DB. Check test link by DB")
    async def test_db(self):
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

    @allure.description("Bruteforce DB method")
    async def test_write_file_history_bruteforce(self):
        assert await tools.fuzzer(db.write_file_history, hard_mode=debug.Switches.IS_HARD_MODE)

    @allure.description("Bruteforce DB method")
    async def test_filter_by_history_bruteforce(self):
        assert await tools.fuzzer(db.filter_by_history, hard_mode=debug.Switches.IS_HARD_MODE)
