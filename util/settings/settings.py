from pathlib import Path
from re import sub
from typing import List, Optional, Union

import aiofiles


class Parameter:

    def __init__(self, name: str, value: str):
        if not isinstance(name, str): raise TypeError("Argument 'name' is not 'str' type")
        if not isinstance(value, str): raise TypeError("Argument 'value' is not 'str' type")
        self.name: str = self.name_check(name)
        self.value: str = self.value_check(value)

    def name_check(self, name: str) -> str:
        if not name.isalpha(): raise ValueError("Argument 'name' is incorrect")
        return name[:1000]

    def value_check(self, value: str) -> str:
        if not value: raise ValueError("Argument 'value' is incorrect")
        return value[:1000]


class Settings:
    def __init__(self,
                 path: Union[str, Path] = Path.cwd(),
                 filename: str = "settings.ini"):
        if not isinstance(path, str | Path): raise TypeError("Argument 'path' is not Union[Path, str] type")
        if not isinstance(filename, str): raise TypeError("Argument 'filename' is not 'str' type")
        path = Path(str(path)[:1000])
        self.path: Path = path if path.exists() and path.is_file() else Path.cwd()
        self.filename = sub(r"[^a-zA-Z0-9_\-.]", "", filename)[:255]

    async def write(self, *params: Parameter) -> None:
        assert all(map(lambda param: True if type(param) == Parameter else False, params))
        try:
            async with aiofiles.open(Path(self.path).joinpath(self.filename), "w", encoding="utf-8") as file:
                [await file.writelines(f"{param.name}={param.value}\n") for param in params]
        except IOError as error:
            print("IOError -", error)

    async def read(self) -> Optional[List[Parameter]]:
        try:
            async with aiofiles.open(Path(self.path).joinpath(self.filename), "r", encoding="utf-8") as file:
                settings_list: List[Parameter] = []
                while line := await file.readline():
                    if not line.strip(): continue
                    name, value = line.split("=")
                    if (name := name.strip()) and (value := value.strip()):
                        settings_list.append(Parameter(name, value))
                return settings_list if settings_list else None

        except FileNotFoundError:
            return print("Settings file not found")
        except (UnicodeDecodeError, TypeError):
            return print("Settings file found but corrupted")
        except IOError as error:
            return print("IOError -", error)
