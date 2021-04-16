import pytest

from SuperHelper.Tests import *


class TestFocusEnabler:
    @staticmethod
    @pytest.fixture()
    def setup():
        run("add FocusEnabler")

    @staticmethod
    def test_validate_setup(setup):
        assert "FocusEnabler" in run("list").output

    @staticmethod
    def test_help():
        assert run("focus --help").exit_code == 0

    @staticmethod
    def test_add_single():
        assert run("focus add -c google.com").exit_code == 0

    @staticmethod
    def test_add_single_again():
        assert run("focus add google.com").exit_code == 0

    @staticmethod
    def test_list_single_positive():
        result = run("focus list")
        assert result.exit_code == 0
        assert "google.com" in result.output

    @staticmethod
    def test_remove_single():
        assert run("focus remove -c google.com").exit_code == 0

    @staticmethod
    def test_list_single_negative():
        result = run("focus list")
        assert result.exit_code == 0
        assert "google.com" not in result.output

    @staticmethod
    def test_add_multiple():
        assert run("focus add facebook.com youtube.com").exit_code == 0

    @staticmethod
    def test_list_multiple_positive():
        result = run("focus list")
        assert result.exit_code == 0
        assert "facebook.com" in result.output
        assert "youtube.com" in result.output

    @staticmethod
    def test_remove_multiple():
        assert run("focus remove -c facebook.com youtube.com").exit_code == 0

    @staticmethod
    def test_list_multiple_negative():
        result = run("focus list")
        assert result.exit_code == 0
        assert "facebook.com" not in result.output
        assert "youtube.com" not in result.output

    @staticmethod
    def test_add_same():
        assert run("focus add facebook.com facebook.com").exit_code == 0

    @staticmethod
    def test_remove_same():
        assert run("focus remove -c facebook.com facebook.com").exit_code == 0

    @staticmethod
    def test_add_invalid():
        assert run("focus add 12345").exit_code == 1

    @staticmethod
    def test_remove_invalid():
        assert run("focus remove -c 12345").exit_code == 1

    @staticmethod
    def test_get_input_prompt():
        from SuperHelper.Modules.FocusEnabler.__main__ import get_input_prompt
        assert type(get_input_prompt("TEST")) == str
