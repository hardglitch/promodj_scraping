import functools
import re
import secrets
import string
import time
from typing import Any, Callable


def perf_counter_decorator() -> Any:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.perf_counter()
                print(f"Work time - {end-start}")
        return wrapped
    return wrapper


def perf_counter_function(func: Callable, *args, **kwargs) -> Any:
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    print(f"Work time - {end - start}")
    return result


def dict_value_sort(dictionary: dict, asc: bool = True) -> dict:
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=not asc)}


def clear_path(path: str):
    return re.sub(r"[^\w\(\)\\\/\[\]\.\,\+\-\&\ \=\']", "", path)


def random_string(max_length: int = 1, path_friendly: bool = False) -> str:
    rnd_str = "".join((secrets.choice(string.printable) for _ in range(secrets.choice(range(max_length)))))
    return rnd_str if not path_friendly else clear_path(rnd_str)
