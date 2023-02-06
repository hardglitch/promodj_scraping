from pathlib import Path
from typing import List, Tuple

import pytest

from utils.settings.settings import Parameter, Settings

test_setting_filename = "test.ini"

def test_parameter():
    p = Parameter("param", "value")
    assert isinstance(p, Parameter)
    assert isinstance(p.name, str)
    assert isinstance(p.value, str)
    assert p.name.isalpha()
    assert p.name is not None
    assert p.value is not None

def test_settings():
    s = Settings()
    assert isinstance(s, Settings)
    assert isinstance(s.path, str | Path)
    assert isinstance(s.filename, str)
    assert s.path is not None
    assert s.filename is not None

@pytest.mark.asyncio
async def test_settings_write(tmp_path):
    s = Settings(path=tmp_path, filename=test_setting_filename)
    p = (Parameter("ParamOne", "value"),
         Parameter("ParamTwo", "value"),
         Parameter("ParamThree", "value")
    )
    assert isinstance(p, Parameter | Tuple | List)
    for _ in p: assert isinstance(_, Parameter)

    await s.write(*p)
    fullpath = s.path.joinpath(s.filename)
    assert fullpath.exists()
    assert fullpath.is_file()
    assert fullpath.stat().st_size > 0

@pytest.mark.asyncio
async def test_settings_read(tmp_path):
    s = Settings(path=tmp_path, filename=test_setting_filename)
    assert isinstance(s, Settings)
    fullpath = s.path.joinpath(s.filename)
    assert fullpath.exists()
    assert fullpath.is_file()
    assert fullpath.stat().st_size > 0

    p = await s.read()
    assert isinstance(p, Parameter | Tuple | List)
    for _ in p: assert isinstance(_, Parameter)
    Path(s.filename).unlink()
