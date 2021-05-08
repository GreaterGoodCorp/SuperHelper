import pytest

from SuperHelper.Tests import *


class TestPyInit:
    @staticmethod
    @pytest.fixture()
    def setup():
        run("add PyInit")

    @staticmethod
    def test_validate_setup(setup):
        assert "PyInit" in run("list").output

    @staticmethod
    def test_run(test_data_dir):
        run(f"py init --name \"Nguyen Thai Binh\" --email bincity2003@gmail.com {str(test_data_dir / 'test')}")
