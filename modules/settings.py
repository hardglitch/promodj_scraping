import os
import re
from pathlib import PurePath
from typing import AnyStr, List

import aiofiles


class Parameter:

    def __init__(self, name: AnyStr = "", value: AnyStr = ""):
        self.name = name if self.name_check(name) else ""
        self.value = value

    def name_check(self, name) -> bool:
        if not name.isalpha():
            raise "Parameter Name is incorrect"
        return True


class Settings:
    def __init__(self,
                 path: AnyStr = os.getcwd(),
                 name: AnyStr = "settings.ini"):
        self.path = PurePath(path) if os.path.exists(path) else os.getcwd()
        self.name = re.sub(r"[^a-zA-Z0-9_\-.]", "", name)


    async def write(self, params: List[Parameter]):
        async with aiofiles.open(os.path.join(self.path, self.name), "w") as file:
            [await file.writelines(f"{param.name}={param.value}\n") for param in params]


    async def read(self) -> List[Parameter]:
        try:
            async with aiofiles.open(os.path.join(self.path, self.name), "r") as file:

                settings_list = []
                while True:
                    line = await file.readline()
                    if not line: break
                    if line.strip() != "":
                        name, value = line.split("=")
                        name = name.strip()
                        value = value.strip()
                        if name != "" and value != "":
                            settings_list.append(Parameter(name, value))

                return settings_list

        except FileNotFoundError:
            print("Settings file not found")
