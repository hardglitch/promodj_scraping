import allure
import pytest

from modules import debug
from util import tools


@allure.epic("Bruteforce all methods this module")
class TestDebug:

    @allure.description("Bruteforce instance of DebugParam subclass")
    def test_set_attribute_debug_param(self) -> None:
        assert debug.set_attribute_test(debug.Switches.IS_DOWNLOAD)

    @allure.description("Bruteforce instance of Constants subclass")
    def test_set_attribute_constants(self) -> None:
        assert debug.set_attribute_test(debug.Constants)

    @allure.description("Bruteforce instance of Switches class")
    def test_set_attribute_switches(self) -> None:
        assert debug.set_attribute_test(debug.Switches)

    @allure.description("Bruteforce Debug method")
    @pytest.mark.asyncio
    async def test_log_bruteforce(self):
        assert await tools.fuzzer(debug.log, hard_mode=debug.Switches.IS_HARD_MODE)

    @allure.description("Bruteforce Debug method")
    @pytest.mark.asyncio
    async def test_switch_bruteforce(self):
        assert await tools.fuzzer(debug.switch, hard_mode=debug.Switches.IS_HARD_MODE)

    @allure.description("Bruteforce Debug method")
    @pytest.mark.asyncio
    async def test_set_attribute_test_bruteforce(self):
        assert await tools.fuzzer(debug.set_attribute_test, hard_mode=debug.Switches.IS_HARD_MODE)
