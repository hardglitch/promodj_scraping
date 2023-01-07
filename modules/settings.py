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


    async def write_all(self, params: List[Parameter]):
        async with aiofiles.open(os.path.join(self.path, self.name), "w") as file:
            [await file.writelines(f"{param.name}={param.value}\n") for param in params]


    async def read_all(self) -> [Parameter]:
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
            raise FileNotFoundError


    async def get(self, param: Parameter) -> str:
        try:
            async with aiofiles.open(os.path.join(self.path, self.name), "r") as file:
                while Exception != EOFError:
                    line = await file.readline()
                    name, value = line.split("=")
                    if param.name == name.strip():
                        return value.strip()
                raise "Parameter not Found"

        except FileNotFoundError:
            raise FileNotFoundError


    async def change(self, param: Parameter):
        # open + find + read + write
        pass


    async def add(self, param: Parameter):
        # open + write
        async with aiofiles.open(os.path.join(self.path, self.name), "a") as file:
            await file.writelines(f"{param.name}={param.value}")


    async def delete(self, param: Parameter):
        # open + find + delete
        pass

