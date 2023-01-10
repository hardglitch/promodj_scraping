import functools
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
