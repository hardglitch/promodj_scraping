from pathlib import Path
from re import sub
from typing import List, Optional, Union

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper


class Parameter:

    def __init__(self, name: str, value: str):
        if not isinstance(name, str): raise TypeError("'name' is not 'str' type")
        if not isinstance(value, str): raise TypeError("'value' is not 'str' type")
        self.name: str = self.name_check(name)
        self.value: str = self.value_check(value)

    def name_check(self, name: str) -> str:
        if not name.isalpha(): raise ValueError("Parameter Name is incorrect")
        return name[:1000]

    def value_check(self, value: str) -> str:
        if not value: raise ValueError("Parameter Value is incorrect")
        return value[:1000]


class Settings:
    def __init__(self,
                 path: Union[str, Path] = Path.cwd(),
                 filename: str = "settings.ini"):
        if not isinstance(path, str|Path): raise TypeError("'path' is not Union[Path, str] type")
        if not isinstance(filename, str): raise TypeError("'filename' is not 'str' type")
        path = Path(str(path)[:1000])
        self.path: Path = path if path.exists() and path.is_file() else Path.cwd()
        self.filename = sub(r"[^a-zA-Z0-9_\-.]", "", filename)[:255]


    async def write(self, *params: Parameter) -> None:
        assert all(map(lambda param: True if type(param)==Parameter else False, params))
        try:
            async with aiofiles.open(Path(self.path).joinpath(self.filename), "w", encoding="utf-8") as file:
                [await file.writelines(f"{param.name}={param.value}\n") for param in params]
        except IOError as error:
            print("IOError -", error)


    async def read(self) -> Optional[List[Parameter]]:
        try:
            async with aiofiles.open(Path(self.path).joinpath(self.filename), "r", encoding="utf-8") as file:
                assert isinstance(file, AsyncTextIOWrapper)

                settings_list = []
                while line := await file.readline():
                    if line.strip():
                        name, value = line.split("=")
                        name = name.strip()
                        value = value.strip()
                        if name and value:
                            settings_list.append(Parameter(name, value))

                return settings_list if settings_list else None

        except FileNotFoundError:
            print("Settings file not found")
            return None
        except (UnicodeDecodeError, TypeError):
            print("Settings file found but corrupted")
            return None
        except IOError as error:
            print("IOError -", error)
            return None