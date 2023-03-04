import inspect
from typing import Set

import aiosqlite

from data.data import CONST
from data.messages import MESSAGES
from modules import debug


async def create_history_db() -> None:
    try:
        async with aiosqlite.connect(database=CONST.DB_NAME) as db_connection:
            sql_request = """CREATE TABLE IF NOT EXISTS file_history(link TEXT NOT NULL, date INTEGER NOT NULL);"""
            await db_connection.execute(sql_request)
    except aiosqlite.DatabaseError as error:
        debug.log(f"DB Error in {inspect.stack()[0][3]} -", error)


async def write_file_history(link: str, date: int) -> None:
    if not link or not isinstance(link, str): return debug.log(MESSAGES.Errors.NoLinkToWrite)
    if not date or not isinstance(date, int): return debug.log(MESSAGES.Errors.NoDate)

    try:
        async with aiosqlite.connect(database=CONST.DB_NAME) as db_connection:
            sql_request = """INSERT INTO file_history VALUES(?, ?)"""
            await db_connection.execute(sql_request, (link, abs(date)))
            await db_connection.commit()
    except aiosqlite.DatabaseError as error:
        debug.log(f"DB Error in {inspect.stack()[0][3]} -", error)


async def filter_by_history(found_links: Set[str]) -> Set[str]:
    if not found_links or\
       not isinstance(found_links, Set) or\
       not all(map(lambda x: True if type(x)==str else False, found_links)):
            debug.log(MESSAGES.Errors.NoLinksToFiltering)
            return set()
    try:
        async with aiosqlite.connect(CONST.DB_NAME) as db_connection:
            sql_request = """SELECT link FROM file_history LIMIT 100000"""
            sql_cursor: aiosqlite.Cursor = await db_connection.execute(sql_request)
            records: Set[str] = set(record[0] for record in await sql_cursor.fetchall())
            return found_links - records
    except aiosqlite.DatabaseError as error:
        debug.log(f"DB Error in {inspect.stack()[0][3]} -", error)
        return found_links
    except TypeError as error:
        debug.log(f"TypeError in {inspect.stack()[0][3]} -", error)
        return found_links
