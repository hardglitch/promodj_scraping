import re
import secrets
import string
import time
from functools import wraps
from typing import Any, Callable, Dict


def perf_counter_decorator() -> Any:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            try: return await func(*args, **kwargs)
            finally: print(f"Work time - {time.perf_counter()-start_time}")
        return wrapped
    return wrapper


async def perf_counter_function(func: Callable, *args: Any, **kwargs: Any) -> Any:
    start_time = time.perf_counter()
    try: return await func(*args, **kwargs)
    finally: print(f"Work time - {time.perf_counter() - start_time}")


def dict_value_sort(dictionary: Dict[Any, Any], asc: bool = True) -> Dict[Any, Any]:
    return {k:v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=not asc)}


def clear_path(path: str) -> str:
    return re.sub(r"[^\w\(\)\\\/\[\]\.\,\+\-\&\ \=\']", "", path)


def clear_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_\-.]", "", filename)[:255]


def random_string(max_length: int = 1, path_friendly: bool = False) -> str:
    rnd_str = "".join((secrets.choice(string.printable) for _ in range(secrets.choice(range(max_length)))))
    return rnd_str if not path_friendly else clear_path(rnd_str)


def byte_dumb(cycles: int = 1) -> bytes:
    """1 cycle = 100 bytes = 1 string.printable"""
    return b"".join(string.printable.encode() for _ in range(cycles))
