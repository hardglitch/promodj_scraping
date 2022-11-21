import functools
import time
from typing import Callable, Any


def async_timer():
    def wrapper(function: Callable) -> Callable:
        @functools.wraps(function)
        async def wrapped(*args, **kwargs) -> Any:
            start = time.time()
            try:
                return await function(*args, **kwargs)
            finally:
                end = time.time()
                delta = end - start
                print(f"Work time - {delta}")
        return wrapped
    return wrapper
