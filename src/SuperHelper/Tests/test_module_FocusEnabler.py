import sys

import pytest

from SuperHelper.Core import main_entry


@pytest.fixture(scope="module", autouse=True)
def add_focus():
    sys.argv = ["helper", "add", "FocusEnabler"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_help():
    sys.argv = ["helper", "focus", "--help"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_add_single():
    sys.argv = ["helper", "focus", "add", "google.com"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_add_multiple():
    sys.argv = ["helper", "focus", "add", "facebook.com", "youtube.com"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_add_invalid():
    sys.argv = ["helper", "focus", "add", "123123"]
    with pytest.raises(SystemExit, match=r"1"):
        main_entry()


def test_remove_single():
    sys.argv = ["helper", "focus", "remove", "-c", "google.com"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_remove_multiple():
    sys.argv = ["helper", "focus", "remove", "-c", "facebook.com", "youtube.com"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_remove_invalid():
    sys.argv = ["helper", "focus", "remove", "-c", "123123"]
    with pytest.raises(SystemExit, match=r"1"):
        main_entry()


def test_list():
    sys.argv = ["helper", "focus", "list"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()
