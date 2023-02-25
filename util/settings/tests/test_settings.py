from pathlib import Path
from typing import List, Set, Tuple

import aiofiles
import pytest

from util.settings.settings import Parameter, Settings

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
async def test_settings_write_read(tmp_path):
    s = Settings(path=tmp_path, filename=test_setting_filename)
    assert isinstance(s, Settings)

    p = (Parameter("ParamOne", "value"),
         Parameter("ParamTwo", "value"),
         Parameter("ParamThree", "value")
    )
    assert isinstance(p, Parameter | Tuple | List | Set)
    for _ in p: assert isinstance(_, Parameter)

    await s.write(*p)
    fullpath = s.path.joinpath(s.filename)
    assert fullpath.exists()
    assert fullpath.is_file()
    assert fullpath.stat().st_size > 0

    p_get = await s.read()
    p_exp = list(p)
    assert isinstance(p_get, List)
    for i, param in enumerate(p_get):
        assert isinstance(param, Parameter)
        assert param.name == p_exp[i].name
        assert param.value == p_exp[i].value

    Path(s.filename).unlink()

@pytest.mark.asyncio
async def test_settings_base_illegal_read(tmp_path):
    s = Settings(path=tmp_path, filename=test_setting_filename)
    assert isinstance(s, Settings)

    base_test_parameters = [
        "",
        "      ",
        " = \n = ",
        "2 = ",
        "2=",
        "= 2  ",
        "=",
        "a=",
    ]

    fullpath = s.path.joinpath(s.filename)
    for p in base_test_parameters:
        async with aiofiles.open(fullpath, "w") as file:
            await file.writelines(p)
        assert fullpath.exists()
        assert fullpath.is_file()
        assert not await s.read()

    Path(s.filename).unlink()
