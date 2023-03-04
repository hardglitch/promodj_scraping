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
    assert await tools.fuzzer(debug.log)

@pytest.mark.asyncio
async def test_switch_bruteforce():
    assert await tools.fuzzer(debug.switch)

@pytest.mark.asyncio
async def test_set_attribute_test_bruteforce():
    assert await tools.fuzzer(debug.set_attribute_test)
