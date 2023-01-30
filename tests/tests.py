import string
from typing import Any, Callable, Iterable

from qasync import QEventLoop

from modules.gui import MainWindow
from tests.config import Config
from utils import tools
from utils.settings import Parameter, Settings

FULL_CHAOS: int = 0
RANDOM_BUT_SETTINGS_TYPE: int = 1
LEGAL_SETTINGS_TYPE: int = 2
LEGAL_PARAMETERS = LEGAL_SETTINGS = 3

class MockParameter(Parameter):
    if Config.DEBUG and Config.MOCK_Parameter:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name, self.value = args


class MockSettings(Settings):
    if Config.DEBUG and Config.MOCK_Settings:
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.path, self.name = args

        def read(self, *args: Any) -> Any:
            return args


class MockMainWindow(MainWindow):
    if Config.DEBUG and Config.MOCK_MainWindow:
        def __init__(self, *args, settings: Settings = None, **kwargs):
            super().__init__(*args, **kwargs)
            self.settings_file = settings


def test(obj: Callable, loop: QEventLoop = None, params_range: int = 5,
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

    if mode in [LEGAL_SETTINGS_TYPE, LEGAL_PARAMETERS, LEGAL_SETTINGS]:
        for _ in range(cycles):
            print(f"{_*100/cycles: <4.1f}", end="")
            try:
                param1 = tools.random_string(10000, path_friendly=True)
                param2 = tools.random_string(10000, path_friendly=True)
                if mode == LEGAL_SETTINGS_TYPE: obj(loop=loop, settings=Settings(param1, param2))
                elif mode == LEGAL_PARAMETERS:
                    __ = obj(param1, param2)
                    if print_process: print(__)
            except AssertionError:
                if print_process: print(f"ERROR CAUGHT - '{obj.__name__}'")
            except ValueError:
                if print_process: print(f"ERROR CAUGHT - '{obj.__name__}'")
            finally:
                print("", end="\r")
    else:
        BASE_TYPES = (1, -1, 0, 0.1, range(10000), "s")
        LIST = list(BASE_TYPES)
        BASE_DICTS = (({x: y} for x in ((*BASE_TYPES, LIST)) if not isinstance(x, Iterable)) for y in (*BASE_TYPES, LIST))
        SPECIAL_CHARS = string.punctuation
        TEST_PARAMETERS = (*BASE_TYPES, LIST, *[([x for x in y]) for y in BASE_DICTS], *(SPECIAL_CHARS))

        recursive_func(n=params_range)

    print(f"OK - '{obj.__name__}' in {mode=} tested.")


def mock_main_window(loop: QEventLoop):
    if Config.DEBUG:
        if Config.MOCK_Parameter: test(obj=MockParameter, mode=FULL_CHAOS)
        if Config.MOCK_Parameter: test(obj=MockParameter, mode=LEGAL_PARAMETERS)
        if Config.MOCK_Settings: test(obj=MockSettings, mode=FULL_CHAOS)
        if Config.MOCK_Settings: test(obj=MockSettings, mode=LEGAL_SETTINGS)
        if Config.MOCK_MainWindow: test(obj=MockMainWindow, loop=loop, mode=FULL_CHAOS)
        if Config.MOCK_MainWindow: test(obj=MockMainWindow, loop=loop, mode=RANDOM_BUT_SETTINGS_TYPE)
        if Config.MOCK_MainWindow: test(obj=MockMainWindow, loop=loop, mode=LEGAL_SETTINGS_TYPE)


