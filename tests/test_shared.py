from data.data import Data
from modules.shared import CurrentValues

def test_set_attribut():
    try:
        CurrentValues.arg = 1
    except:
        assert AttributeError

def test_set_wrong_attribut_types():
    try:
        CurrentValues.session = 23
        CurrentValues.quantity = "str"
        CurrentValues.genre = 1
        CurrentValues.form = 12
        CurrentValues.is_period = [1,3]
        CurrentValues.is_file_history = {1:2}
        CurrentValues.is_rewrite_files = "genre"
        CurrentValues.is_lossless = -45
        CurrentValues.threads = 2.0
        CurrentValues.download_dir = -3.5
        CurrentValues.total_files = "1"
        CurrentValues.total_downloaded = 1.4
        CurrentValues.total_size = -2
        CurrentValues.total_downloaded_files = ["-ABC"]
    except:
        assert TypeError

def test_set_wrong_value():
    CurrentValues.genre = "My Favorite Genre"
    assert CurrentValues.genre == Data.DefaultValues.genre

    CurrentValues.form = "Super Form"
    assert CurrentValues.form == Data.DefaultValues.form

    CurrentValues.quantity = -3
    assert CurrentValues.quantity == 0

    CurrentValues.quantity = 1100
    assert CurrentValues.quantity == Data.MaxValues.quantity

    CurrentValues.threads = -3
    assert CurrentValues.threads == 1

    CurrentValues.threads = 11
    assert CurrentValues.threads == Data.MaxValues.threads

    CurrentValues.total_files = -3
    assert CurrentValues.total_files == 0

    CurrentValues.total_files = 1100
    assert CurrentValues.total_files == Data.MaxValues.quantity

    CurrentValues.total_downloaded_files = -3
    assert CurrentValues.total_downloaded_files == 0

    CurrentValues.total_downloaded_files = 1100
    assert CurrentValues.total_downloaded_files == Data.MaxValues.quantity

    CurrentValues.total_downloaded = -3
    assert CurrentValues.total_downloaded == 0

    CurrentValues.total_size = -3
    assert CurrentValues.total_size == 0
