import allure
from data.data import Data
from modules import debug
from modules.shared import CurrentValues
from util import tools


@ allure.epic("Bruteforce the 'Shared' methods and attributes")
class BruteforceShared:
    def test_set_wrong_attribute(self):
        debug.set_attribute_test(CurrentValues)

    async def test_set_wrong_attribute_in_init(self):
        assert await tools.fuzzer(CurrentValues.__init__, 15, hard_mode=debug.Switches.IS_HARD_MODE)

    def test_download_dir_bruteforce(self):
        CurrentValues.genre = "My Favorite Genre"
        assert CurrentValues.genre == Data.DefaultValues.genre

        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.download_dir = value
            except: assert TypeError
            assert isinstance(CurrentValues.download_dir, str)

    def test_form_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.form = value
            except: assert TypeError
            assert CurrentValues.form == Data.DefaultValues.form

    def test_quantity_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.quantity = value
            except: assert TypeError
            assert isinstance(CurrentValues.quantity, int) and 0 <= CurrentValues.quantity <= Data.MaxValues.quantity

    def test_threads_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.threads = value
            except: assert TypeError
            assert isinstance(CurrentValues.threads, int) and 0 <= CurrentValues.threads <= Data.MaxValues.threads

    def test_total_files_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.total_files = value
            except: assert TypeError
            assert isinstance(CurrentValues.total_files, int) and 0 <= CurrentValues.total_files <= Data.MaxValues.quantity

    def test_total_downloaded_files_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.total_downloaded_files = value
            except: assert TypeError
            assert isinstance(CurrentValues.total_downloaded_files, int) \
                   and 0 <= CurrentValues.total_downloaded_files <= Data.MaxValues.quantity

    def test_total_downloaded_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.total_downloaded = value
            except: assert TypeError
            assert isinstance(CurrentValues.total_downloaded, int) and CurrentValues.total_downloaded >= 0

    def test_total_size_bruteforce(self):
        for value in tools.BRUTAL_TEST_PARAMETERS if debug.Switches.IS_HARD_MODE else tools.TEST_PARAMETERS:
            try: CurrentValues.total_size = value
            except: assert TypeError
            assert isinstance(CurrentValues.total_size, int) and CurrentValues.total_size >= 0
