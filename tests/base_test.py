import asyncio
import string
import sys
from typing import Callable, Iterable

from PyQt6.QtWidgets import QApplication

from modules.gui import MainWindow
from utils import tools
from utils.settings.settings import Settings

FULL_CHAOS: int = 0
HALF_LEGAL_ARGUMENTS: int = 1
LEGAL_ARGUMENTS: int = 2

BASE_TYPES = (1, -1, 0, 0.1, range(10000), "s")
LIST = list(BASE_TYPES)
DICTS = (({x: y} for x in (*BASE_TYPES, LIST) if not isinstance(x, Iterable)) for y in (*BASE_TYPES, LIST))
SPECIAL_CHARS = string.punctuation
TEST_PARAMETERS = (*BASE_TYPES, LIST, *[([x for x in y]) for y in DICTS], *SPECIAL_CHARS)

TEST_LOOP = asyncio.new_event_loop()

class MockSettings(Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path, self.name = args

class MockMainWindow(MainWindow):
    def __init__(self, *args, settings: Settings = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._loop = TEST_LOOP
        self._settings_file = settings

def test(obj: Callable, params_range: int = 5,
         cycles: int = 1000, print_process: bool = False, mode: int = FULL_CHAOS):

    def recursive_func(*args, n: int = 0):
        for tp in TEST_PARAMETERS:
            if n > 0:
                n -= 1
                recursive_func(*args, tp, n=n)
            try:
                if mode == FULL_CHAOS: _ = obj(*args, tp)
                else: _ = obj(MockSettings(*args, tp))
                if print_process: print(_)
            except AssertionError:
                if print_process: print(f"ERROR CAUGHT - '{obj.__name__}' -", *args, tp)
            except TypeError as error:
                if str(error).find("positional argument") < 0 and obj.__name__ != "MockMainWindow": raise error
            except ValueError as error:
                if str(error).find("not enough values to unpack") < 0: raise error

    if mode == LEGAL_ARGUMENTS:
        for _ in range(cycles):
            print(f"{_*100/cycles: <4.1f}", end="")
            try:
                param1 = tools.random_string(1010, path_friendly=True)
                param2 = tools.random_string(1010, path_friendly=True)
                if obj.__name__ == "MockMainWindow":
                    obj(loop=TEST_LOOP, settings=Settings(param1, param2))
                else: obj(param1, param2)
            except AssertionError:
                if print_process: print(f"ERROR CAUGHT - '{obj.__name__}'")
            except ValueError:
                if print_process: print(f"ERROR CAUGHT - '{obj.__name__}'")
            finally:
                print("", end="\r")
    else:
        recursive_func(n=params_range)

    print(f"OK - '{obj.__name__}' in {mode=} tested.")

@tools.perf_counter_decorator()
def all_tests():
    test(obj=MockMainWindow, mode=FULL_CHAOS)
    test(obj=MockMainWindow, mode=HALF_LEGAL_ARGUMENTS)
    test(obj=MockMainWindow, mode=LEGAL_ARGUMENTS)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    asyncio.set_event_loop(TEST_LOOP)
    all_tests()
