import pytest

from SuperHelper.Tests import *


class TestStenographer:
    @staticmethod
    @pytest.fixture()
    def setup():
        run("add Stenographer")

    @staticmethod
    def test_validate_setup(setup):
        assert "Stenographer" in run("list").output

    @staticmethod
    def test_help():
        assert run("steg --help").exit_code == 0
