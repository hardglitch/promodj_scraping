from data.data import Data
from modules.shared import CurrentValues


def test_set_attribute():
    try:
        CurrentValues.arg = 1
    except:
        assert AttributeError


def test_set_wrong_attribute_types():
    test_values = [1, 2.0, -10, "1", {1:2}, ["f", 1], "genre", ()]
    for attr in CurrentValues.__slots__:
        for value in test_values:
            try:
                setattr(CurrentValues, attr[2:], value)
            except TypeError:
                assert TypeError
            except ValueError:
                assert ValueError


def test_set_incorrect_value():
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
