from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


@dataclass()
class Helpers:
    GUI = True

    def gui_disabler(self) -> Any:
        def wrapper(func: Callable) -> Callable:
            @wraps(func)
            def wrapped(*args: Any, **kwargs: Any):
                return func(*args, **kwargs) if self.GUI else None
            return wrapped
        return wrapper

helpers = Helpers()