import functools
import re
import secrets
import string
import time
from typing import Any, Callable


def performance_counter():
    def wrapper(function: Callable) -> Callable:
        @functools.wraps(function)
        async def wrapped(*args, **kwargs) -> Any:
            start = time.perf_counter()
            try:
                return await function(*args, **kwargs)
            finally:
                end = time.perf_counter()
                print(f"Work time - {end-start}")
        return wrapped
    return wrapper


def dict_value_sort(dictionary: dict, asc: bool = True) -> dict:
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=not asc)}


def clear_path(path: str):
    return re.sub(r"[^\w\(\)\\\/\[\]\.\,\+\-\&\ \=\']", "", path)


def random_string(max_length: int = 1, path_friendly: bool = False) -> str:
    rnd_str = ""
    for n in range(secrets.choice(range(max_length))):
        rnd_str += secrets.choice(string.printable)
    return rnd_str if not path_friendly else clear_path(rnd_str)
