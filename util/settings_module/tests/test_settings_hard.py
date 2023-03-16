import string
from typing import Callable, Generator, Iterable, Tuple

from util import tools
from util.settings_module.settings_module import Parameter, Settings

FULL_CHAOS: int = 0
LEGAL_ARGUMENTS: int = 2

BASE_TYPES: Tuple = (1, -1, 0, 0.1, range(10000), "s")
LIST = list(BASE_TYPES)
DICTS: Generator = (({x: y} for x in (*BASE_TYPES, LIST) if not isinstance(x, Iterable)) for y in (*BASE_TYPES, LIST))
SPECIAL_CHARS: str = string.punctuation
TEST_PARAMETERS: Tuple = (*BASE_TYPES, LIST, *[([x for x in y]) for y in DICTS], *SPECIAL_CHARS)


class MockParameter(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name, self.value = args


class MockSettings(Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path, self.name = args


def hard_test(obj: Callable, params_range: int = 5, cycles: int = 1000, mode: int = FULL_CHAOS) -> bool:

    def recursive_func(*args, n: int = 0):
        for tp in TEST_PARAMETERS:
            if n > 0:
                n -= 1
                recursive_func(*args, tp, n=n)
            try:
                if mode == FULL_CHAOS: _ = obj(*args, tp)
                else: _ = obj(MockSettings(*args, tp))
            except TypeError as error:
                if all([str(error).find(text) < 0 for text in [
                    "positional argument",
                    "is not Union[Path, str] type",
                    "is not 'str' type"
                ]]):
                    raise error
            except ValueError as error:
                if str(error).find("not enough values to unpack") < 0: raise error

    if mode == LEGAL_ARGUMENTS:
        for _ in range(cycles):
            # print(f"{_*100/cycles: <4.1f}", end="")
            try:
                param1 = tools.random_string(1010, path_friendly=True)
                param2 = tools.random_string(1010, path_friendly=True)
                obj(param1, param2)
            except AssertionError: pass
            except ValueError: pass
            # finally: print("", end="\r")
    else:

        recursive_func(n=params_range)

    # print(f"OK - '{obj.__name__}' in {mode=} tested.")
    return True

def test_parameter_full_chaos():
    assert hard_test(obj=MockParameter, mode=FULL_CHAOS)

def test_parameter_legal_arguments():
    assert hard_test(obj=MockParameter, mode=LEGAL_ARGUMENTS)

def test_settings_full_chaos():
    assert hard_test(obj=MockSettings, mode=FULL_CHAOS)

def test_settings_legal_arguments():
    assert hard_test(obj=MockSettings, mode=LEGAL_ARGUMENTS)

