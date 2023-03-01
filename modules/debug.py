import inspect
import logging
from dataclasses import dataclass
from functools import wraps
from time import gmtime, strftime
from typing import Any, Callable, Optional


@dataclass()
class DebugParam:
    name: str
    value: bool

@dataclass(slots=True)
class __Constants:
    IS_GUI = DebugParam("IS_GUI", True)
    IS_DOWNLOAD = DebugParam("IS_DOWNLOAD", True)       # download simulation (True = Real)
    IS_WRITE_FILE = DebugParam("IS_WRITE_FILE", True)
    IS_PRINTING: bool = True                            # console output
    IS_LOGGING: bool = True
    LOG_FILE = "logging.log"

Constants = __Constants()


def log(message: str, error: Optional[Exception] = None, is_exit: bool = False) -> None:
    assert isinstance(message, str)
    assert isinstance(error, Exception | None)
    assert isinstance(is_exit, bool)
    message = message[:1000]
    if Constants.IS_LOGGING:
        tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.basicConfig(filename=Constants.LOG_FILE, encoding="utf-8", level=logging.ERROR)
        logging.exception(tm) if error else logging.error(tm + " - " + message)
    if is_exit: exit(message + (" - " + str(error) if error else ""))


def print_message(*args: Any, **kwargs: Any) -> None:
    if Constants.IS_PRINTING: print(*args, **kwargs)


def switch(debug_param: DebugParam) -> Any:
    def wrapper(func: Callable):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Constants, debug_param.name):
                    return await func(*args, **kwargs) if debug_param.value else False
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Constants, debug_param.name):
                    return func(*args, **kwargs) if debug_param.value else False
        return wrapped
    return wrapper

