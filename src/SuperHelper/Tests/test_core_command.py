from SuperHelper.Tests import *


class TestCore:
    @staticmethod
    def test_add_single():
        assert run("add FocusEnabler").exit_code == 0

    @staticmethod
    def test_list_single_positive():
        result = run("list")
        assert result.exit_code == 0
        assert "FocusEnabler" in result.output
        assert "Stenographer" not in result.output

    @staticmethod
    def test_remove_single():
        assert run("remove FocusEnabler").exit_code == 0

    @staticmethod
    def test_list_single_negative():
        result = run("list")
        assert result.exit_code == 0
        assert "FocusEnabler" not in result.output
        assert "Stenographer" not in result.output

    @staticmethod
    def test_add_multiple():
        assert run("add FocusEnabler Stenographer").exit_code == 0

    @staticmethod
    def test_list_multiple_positive():
        result = run("list")
        assert result.exit_code == 0
        assert "FocusEnabler" in result.output
        assert "Stenographer" in result.output

    @staticmethod
    def test_remove_multiple():
        assert run("remove FocusEnabler Stenographer").exit_code == 0

    @staticmethod
    def test_list_multiple_negative():
        result = run("list")
        assert result.exit_code == 0
        assert "FocusEnabler" not in result.output
        assert "Stenographer" not in result.output

    @staticmethod
    def test_list_all():
        result = run("list -a")
        assert result.exit_code == 0
        assert "FocusEnabler" in result.output
        assert "Stenographer" in result.output

    @staticmethod
    def test_add_same():
        assert run("add FocusEnabler FocusEnabler").exit_code == 0

    @staticmethod
    def test_remove_same():
        assert run("remove FocusEnabler FocusEnabler").exit_code == 0

    @staticmethod
    def test_add_invalid():
        assert run("add test").exit_code == 1

    @staticmethod
    def test_remove_invalid():
        assert run("remove test").exit_code == 1

    @staticmethod
    def test_list_negative():
        assert run("list").exit_code == 0
