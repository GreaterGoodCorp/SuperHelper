from SuperHelper.Tests import *


class TestCore:
    @staticmethod
    def test_add_single():
        assert run("add FocusEnabler").exit_code == 0

    @staticmethod
    def test_remove_single():
        assert run("remove FocusEnabler").exit_code == 0

    @staticmethod
    def test_add_multiple():
        assert run("add FocusEnabler Stenographer").exit_code == 0

    @staticmethod
    def test_remove_multiple():
        assert run("remove FocusEnabler Stenographer").exit_code == 0

    @staticmethod
    def test_add_invalid():
        assert run("add test").exit_code == 1

    @staticmethod
    def test_remove_invalid():
        assert run("remove test").exit_code == 1

    @staticmethod
    def test_list():
        assert run("list").exit_code == 0
