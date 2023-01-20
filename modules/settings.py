import re
from pathlib import Path
from typing import AnyStr, List

import aiofiles


class Parameter:

    def __init__(self, name: AnyStr = "", value: AnyStr = ""):
        self.name: AnyStr = name if self.name_check(name) else ""
        self.value: AnyStr = value

    def name_check(self, name) -> bool:
        if not name.isalpha():
            raise "Parameter Name is incorrect"
        return True


class Settings:
    def __init__(self,
                 path: AnyStr = Path.cwd(),
                 name: AnyStr = "settings.ini"):
        self.path = path if Path(path).exists() and Path(path).is_file() else Path.cwd()
        self.name = re.sub(r"[^a-zA-Z0-9_\-.]", "", name)


    async def write(self, *params: Parameter):
        try:
            async with aiofiles.open(Path.joinpath(self.path, self.name), "w", encoding="utf-8") as file:
                [await file.writelines(f"{param.name}={param.value}\n") for param in params]
        except IOError:
            pass


    async def read(self) -> List[Parameter]:
        try:
            async with aiofiles.open(Path.joinpath(self.path, self.name), "r", encoding="utf-8") as file:

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
