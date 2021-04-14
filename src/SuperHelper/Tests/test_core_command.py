import sys
from subprocess import Popen

import pytest

from SuperHelper.Core import main_entry
from SuperHelper.Core.Config.config_class import Singleton


@pytest.fixture(autouse=True)
def create_and_clean_config():
    Popen(["make", "clean"])
    sys.argv = ["helper", "add", "Stenographer"]
    with pytest.raises(SystemExit, match=r"0"):
        main_entry()
    yield
    Popen(["make", "clean"])


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
