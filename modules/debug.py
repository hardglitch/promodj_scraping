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

@dataclass(slots=True, frozen=True)
class __Constants:
    LOG_FILE = "logging.log"

Constants = __Constants()

@dataclass(slots=True)
class __Switches:
    IS_PRINTING: bool = True    # output to the console additional info
    IS_LOGGING: bool = True

    # -- file.py --
    IS_GUI = DebugParam("IS_GUI", True)
    IS_DOWNLOAD = DebugParam("IS_DOWNLOAD", True)
    IS_GET_FILE = DebugParam("IS_GET_FILE", True)
    IS_WRITE_FILE = DebugParam("IS_WRITE_FILE", True)

Switches = __Switches()


def log(message: str, error: Optional[Exception] = None, is_exit: bool = False) -> None:
    assert isinstance(message, str)
    assert isinstance(error, Exception | None)
    assert isinstance(is_exit, bool)
    message = message[:1000]
    if Switches.IS_LOGGING:
        tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.basicConfig(filename=Constants.LOG_FILE, encoding="utf-8", level=logging.ERROR)
        logging.exception(tm) if error else logging.error(tm + " - " + message)
    if is_exit: exit(message + (" - " + str(error) if error else ""))


def print_message(*args: Any, **kwargs: Any) -> None:
    if Switches.IS_PRINTING: print(*args, **kwargs)


def switch(debug_param: DebugParam) -> Any:
    def wrapper(func: Callable):
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Switches, debug_param.name):
                    return await func(*args, **kwargs) if debug_param.value else False
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Switches, debug_param.name):
                    return func(*args, **kwargs) if debug_param.value else False
        return wrapped
    return wrapper

