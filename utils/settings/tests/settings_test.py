import string
from typing import Any, Callable, Generator, Iterable, Tuple

from utils import tools
from utils.settings.settings import Parameter, Settings

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

    def read(self, *args: Any) -> Any:
        return args


def test(obj: Callable, params_range: int = 5, cycles: int = 1000, mode: int = FULL_CHAOS):

    def recursive_func(*args, n: int = 0):
        for tp in TEST_PARAMETERS:
            if n > 0:
                n -= 1
                recursive_func(*args, tp, n=n)
            try:
                if mode == FULL_CHAOS: _ = obj(*args, tp)
                else: _ = obj(MockSettings(*args, tp))
            except AssertionError: pass
            except TypeError as error:
                if str(error).find("positional argument") < 0: raise error
            except ValueError as error:
                if str(error).find("not enough values to unpack") < 0: raise error

    if mode == LEGAL_ARGUMENTS:
        for _ in range(cycles):
            print(f"{_*100/cycles: <4.1f}", end="")
            try:
                param1 = tools.random_string(1010, path_friendly=True)
                param2 = tools.random_string(1010, path_friendly=True)
                obj(param1, param2)
            except AssertionError: pass
            except ValueError: pass
            finally: print("", end="\r")
    else:

        recursive_func(n=params_range)

    print(f"OK - '{obj.__name__}' in {mode=} tested.")

@tools.perf_counter_decorator()
def all_tests():
    test(obj=MockParameter, mode=FULL_CHAOS)
    test(obj=MockParameter, mode=LEGAL_ARGUMENTS)
    test(obj=MockSettings, mode=FULL_CHAOS)
    test(obj=MockSettings, mode=LEGAL_ARGUMENTS)


if __name__ == "__main__":
    all_tests()
