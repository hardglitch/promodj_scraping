import pytest

from modules import debug
from util import tools


def test_set_attribute_debug_param() -> None:
    assert debug.set_attribute_test(debug.Switches.IS_DOWNLOAD)

def test_set_attribute_constants() -> None:
    assert debug.set_attribute_test(debug.Constants)

def test_set_attribute_switches() -> None:
    assert debug.set_attribute_test(debug.Switches)

@pytest.mark.asyncio
async def test_log_bruteforce():
    assert await tools.fuzzer(debug.log, hard_mode=debug.Switches.IS_HARD_MODE)

@pytest.mark.asyncio
async def test_switch_bruteforce():
    assert await tools.fuzzer(debug.switch, hard_mode=debug.Switches.IS_HARD_MODE)

@pytest.mark.asyncio
async def test_set_attribute_test_bruteforce():
    assert await tools.fuzzer(debug.set_attribute_test, hard_mode=debug.Switches.IS_HARD_MODE)
