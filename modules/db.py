from typing import Set

import aiosqlite

from modules import debug
from modules.data import Data
from modules.messages import Messages


async def create_history_db():
    try:
        async with aiosqlite.connect(database=Data.DB_NAME) as db_connection:
            sql_request = """CREATE TABLE IF NOT EXISTS file_history(link TEXT NOT NULL, date INTEGER NOT NULL);"""
            await db_connection.execute(sql_request)
    except aiosqlite.DatabaseError as error:
        debug.log("DB Error -", error)


async def write_file_history(link: str, date: int):
    if link is None: exit(Messages.Errors.NoLinkToWrite)
    if date is None: exit(Messages.Errors.NoDate)
    assert isinstance(link, str) and isinstance(date, int)

    try:
        async with aiosqlite.connect(database=Data.DB_NAME) as db_connection:
            sql_request = """INSERT INTO file_history VALUES(?, ?)"""
            await db_connection.execute(sql_request, (link, abs(date)))
            await db_connection.commit()
    except aiosqlite.DatabaseError as error:
        debug.log("DB Error -", error)


async def filter_by_history(found_links: Set[str]) -> Set[str]:
    assert isinstance(found_links, Set)
    for n in found_links: assert isinstance(n, str)

    try:
        async with aiosqlite.connect(Data.DB_NAME) as db_connection:
            sql_request = """SELECT link FROM file_history LIMIT 100000"""
            sql_cursor: aiosqlite.Cursor = await db_connection.execute(sql_request)
            records: Set[str] = set(record[0] for record in await sql_cursor.fetchall())
            return found_links - records
    except aiosqlite.DatabaseError as error:
        debug.log("DB Error -", error)
    except TypeError as error:
        debug.log("TypeError -", error)
