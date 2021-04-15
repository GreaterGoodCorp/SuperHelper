import sys

import pytest

from SuperHelper.Core import main_entry


def test_add_valid():
    sys.argv = ["helper", "add", "FocusEnabler"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_add_invalid():
    sys.argv = ["helper", "add", "test"]
    with pytest.raises(SystemExit, match=r"1"):
        main_entry()


def test_remove_valid():
    sys.argv = ["helper", "remove", "Stenographer"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()


def test_remove_invalid():
    sys.argv = ["helper", "remove", "test"]
    with pytest.raises(SystemExit, match=r"1"):
        main_entry()


def test_list():
    sys.argv = ["helper", "list"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()
