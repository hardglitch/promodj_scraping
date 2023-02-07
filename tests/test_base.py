import asyncio
from pathlib import Path

import aiohttp

from modules.base import Base
from modules.data import Data
from tests import prerequisites

TEST_LOOP = prerequisites.start()

def test_default_values():
    b = Base(loop=TEST_LOOP)
    assert b.download_dir == Path(Data.DefaultValues.download_dir)
    assert b.genre == Data.DefaultValues.genre
    assert b.form == Data.DefaultValues.form
    assert b.is_lossless == Data.DefaultValues.is_lossless
    assert b.quantity == Data.DefaultValues.quantity
    assert b.is_period == Data.DefaultValues.is_period
    assert b.threads == Data.DefaultValues.threads
    assert b.is_rewrite_files == Data.DefaultValues.is_rewrite_files
    assert b.is_file_history == Data.DefaultValues.is_file_history

    assert b._loop is not None
    assert b._download_future is None
    assert b._session is None

    assert b.progress
    assert b.succeeded
    assert b.total_size == 0
    assert b.total_downloaded == 0

def test_default_types():
    b = Base(loop=TEST_LOOP)
    assert isinstance(b.download_dir, str|Path)
    assert isinstance(b.genre, str)
    assert isinstance(b.form, str)
    assert isinstance(b.is_lossless, bool)
    assert isinstance(b.quantity, int)
    assert isinstance(b.is_period, bool)
    assert isinstance(b.threads, int)
    assert isinstance(b.is_rewrite_files, bool)
    assert isinstance(b.is_file_history, bool)

    assert isinstance(b._loop, asyncio.AbstractEventLoop)
    assert isinstance(b._download_future, asyncio.Future | None)
    assert isinstance(b._session, aiohttp.ClientSession | None)

    assert isinstance(b.total_size, int)
    assert isinstance(b.total_downloaded, int)
