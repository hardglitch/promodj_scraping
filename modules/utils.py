import functools
import time
from typing import Any, Callable


def async_timer():
    def wrapper(function: Callable) -> Callable:
        @functools.wraps(function)
        async def wrapped(*args, **kwargs) -> Any:
            start = time.perf_counter()
            try:
                return await function(*args, **kwargs)
            finally:
                end = time.perf_counter()
                delta = end - start
                print(f"Work time - {delta}")
        return wrapped
    return wrapper

