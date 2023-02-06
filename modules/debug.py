import functools
import logging
from dataclasses import dataclass
from time import gmtime, strftime
from typing import Any, Callable


@dataclass()
class Constants:
    IS_DOWNLOAD = True     # download simulation
    PRINTING: bool = True  # console output
    LOGGING: bool = True
    LOG_FILE = "logging.log"


def log(message: str, error: Exception = None):
    assert isinstance(message, str)
    assert isinstance(error, Exception | None)
    message = message[:1000]
    if Constants.LOGGING:
        tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.basicConfig(filename=Constants.LOG_FILE, encoding="utf-8", level=logging.ERROR)
        logging.exception(tm) if error else logging.error(tm + " - " + message)
    exit(message + (" - " + str(error) if error else ""))


def print_message(*args, **kwargs) -> None:
    if Constants.PRINTING: print(*args, **kwargs)


def is_download() -> Any:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            return await func(*args, **kwargs) if Constants.IS_DOWNLOAD else None
        return wrapped
    return wrapper
