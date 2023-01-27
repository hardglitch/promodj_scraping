import re
from pathlib import Path
from typing import List

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper


# from tests import tests


class Parameter:

    def __init__(self, name: str = None, value: str = None):
        assert isinstance(name, str) and isinstance(value, str)
        self.name: str = self.name_check(name)
        self.value: str = self.value_check(value)

    def name_check(self, name: str) -> str:
        assert isinstance(name, str)
        if not name.isalpha():
            raise ValueError("Parameter Name is incorrect")
        return name[:1000]

    def value_check(self, value: str) -> str:
        assert isinstance(value, str)
        if not value:
            raise "Parameter Value is incorrect"
        return value[:1000]


class Settings:
    def __init__(self,
                 path: str = str(Path.cwd()),
                 name: str = "settings.ini"):
        assert isinstance(path, str) and isinstance(name, str)
        self.path: Path = Path(path[:1000]) if Path(path[:1000]).exists() and Path(path[:1000]).is_file() else Path.cwd()
        self.name = re.sub(r"[^a-zA-Z0-9_\-.]", "", name)[:255]


    async def write(self, *params: Parameter):
        for param in params:
            assert isinstance(param, Parameter)
        try:
            async with aiofiles.open(Path.joinpath(self.path, self.name), "w", encoding="utf-8") as file:
                [await file.writelines(f"{param.name}={param.value}\n") for param in params]
        except IOError as error:
            print("IOError -", error)


    async def read(self) -> List[Parameter]:
        try:
            async with aiofiles.open(Path.joinpath(self.path, self.name), "r", encoding="utf-8") as file:
                assert isinstance(file, AsyncTextIOWrapper)

                settings_list = []
                while line := await file.readline():
                    if line.strip():
                        name, value = line.split("=")
                        name = name.strip()
                        value = value.strip()
                        if name and value:
                            settings_list.append(Parameter(name, value))

                return settings_list

        except FileNotFoundError:
            print("Settings file not found")
        except UnicodeDecodeError:
            print("Settings file found but corrupted")
