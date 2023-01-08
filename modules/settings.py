import os
from typing import List

import aiofiles


class Parameter:

    def __init__(self, name: str, value: str = ""):
        self.name = name if self.name_check(name) else ""
        self.value = value


    def name_check(self, name) -> bool:

        charset = "abcdefghijklmnopqrstuvwxyz"  # utf-8 by default

        try:
            if name != "":
                for char in name:
                    if char.lower() not in charset:
                        return False
                return True
            return False
        except Exception as error:
            raise error


class Settings:
    def __init__(self,
                 path: str = os.getcwd(),
                 name: str = "settings.ini"):
        self.path = path
        self.name = name


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
