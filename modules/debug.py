import logging
from dataclasses import dataclass
from functools import wraps
from inspect import iscoroutinefunction
from time import gmtime, strftime
from typing import Any, Callable, Optional

from data.messages import MESSAGES


@dataclass(slots=True, frozen=True)
class __Constants:
    LOG_FILE: str = "logging.log"

Constants = __Constants()

@dataclass(slots=True)
class DebugParam:
    name: str
    value: bool
    fake_func: Optional[Callable] = None

@dataclass(slots=True)
class __Switches:
    IS_PRINTING: bool = True    # output to the console additional info
    IS_LOGGING: bool = True
    IS_GUI: bool = True

    # -- file.py --
    IS_DOWNLOAD = DebugParam("IS_DOWNLOAD", True)
    IS_GET_FILE = DebugParam("IS_GET_FILE", True)
    IS_WRITE_FILE = DebugParam("IS_WRITE_FILE", True)

    # -- link.py --
    IS_PARSE = DebugParam("IS_PARSE", True)
    IS_WORKER = DebugParam("IS_WORKER", True)

Switches = __Switches()


def log(message: str, error: Optional[Exception] = None, is_exit: bool = False) -> None:
    if not isinstance(message, str) or not message or \
       not isinstance(error, Exception | None) or \
       not isinstance(is_exit, bool):
            return None
    message = message[:1000]
    if Switches.IS_LOGGING:
        tm = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logging.basicConfig(filename=Constants.LOG_FILE, encoding="utf-8", level=logging.ERROR)
        logging.exception(tm) if error else logging.error(tm + " - " + message)
    if is_exit: exit(message + (" - " + str(error) if error else ""))


def print_message(*args: Any, **kwargs: Any) -> None:
    if Switches.IS_PRINTING: print(*args, **kwargs)


def switch(debug_param: DebugParam) -> Any:
    if not isinstance(debug_param, DebugParam): return None
    def wrapper(func: Callable):
        if iscoroutinefunction(func):
            @wraps(func)
            async def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Switches, debug_param.name):
                    if debug_param.fake_func:
                        return await debug_param.fake_func() if iscoroutinefunction(debug_param.fake_func) \
                                else debug_param.fake_func()
                    if debug_param.value: return await func(*args, **kwargs)
                    return False
        else:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                if getattr(Switches, debug_param.name):
                    if debug_param.fake_func: return debug_param.fake_func()
                    if debug_param.value: return func(*args, **kwargs)
                    return False
        return wrapped
    return wrapper


def set_attribute_test(instance: Any) -> bool:
    try: setattr(instance, "new", 1)
    except (AttributeError, TypeError): return True
    else: raise Exception(MESSAGES.Errors.SecurityThreat)
