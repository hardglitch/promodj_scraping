import re
import secrets
import string
import sys
import time
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, Callable, Dict, Iterable


BASE_TYPES = (sys.maxsize, -1, 0, 0.1, range(10000), "", " ", b"s", string.printable)
LIST = list(BASE_TYPES)
DICTS = (({x: y} for x in (*BASE_TYPES, LIST) if not isinstance(x, Iterable)) for y in (*BASE_TYPES, LIST))
SPECIAL_CHARS = string.punctuation
TEST_PARAMETERS = (*BASE_TYPES, LIST, *[([x for x in y]) for y in DICTS], *SPECIAL_CHARS)


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
    return (re.sub(r"[^\w\(\)\\\/\[\]\.\,\+\-\&\ \=\']", "", path)).strip()


def clear_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_\-.]", "", filename)[:255]


def insert_string(old_str: str, patch_str: str, position: int) -> str:
    return old_str[:position] + patch_str + old_str[position:]


def random_string(max_length: int = 1, path_friendly: bool = False) -> str:
    rnd_str = "".join((secrets.choice(string.printable) for _ in range(secrets.choice(range(max_length)))))
    return rnd_str if not path_friendly else clear_path(rnd_str)


def byte_dumb(cycles: int = 1) -> bytes:
    """1 cycle = 100 bytes = 1 string.printable"""
    return b"".join(string.printable.encode() for _ in range(cycles))


BRUTAL_TEST_PARAMETERS = (*TEST_PARAMETERS, *(random_string(1100) for _ in range(50)))

async def fuzzer(obj: Callable, params_range: int = 5, hard_mode: bool = False) -> bool:
    # test_parameters = BRUTAL_TEST_PARAMETERS if hard_mode else TEST_PARAMETERS

    async def recursive_func(*args: Any, n: int = 0) -> None:
        for tp in BRUTAL_TEST_PARAMETERS if hard_mode else TEST_PARAMETERS:
            if n > 0:
                n -= 1
                await recursive_func(*args, tp, n=n)
            try:
                if iscoroutinefunction(obj): await obj(*args, tp)
                else: obj(*args, tp)
            except TypeError as error:
                if str(error).find("positional argument") < 0: raise error
            except ValueError as error:
                if str(error).find("not enough values to unpack") < 0: raise error

    await recursive_func(n=params_range)
    return True
