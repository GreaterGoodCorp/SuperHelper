import pytest

from SuperHelper.Core import run_startup
from SuperHelper.Core.Config import Config, pass_config


class TestConfig:
    @staticmethod
    def test_from_dict():
        assert Config.from_dict(dict()) is None

    @staticmethod
    def test_core_and_no_module():
        @pass_config(core=True, lock=True)
        def test_a(config):
            return config
        run_startup()
        test_a()

    @staticmethod
    def test_no_core_and_module_a():
        @pass_config(module_name="test", lock=True)
        def test_a(config):
            return config
        run_startup()
        test_a()

    @staticmethod
    def test_no_core_and_module_b():
        @pass_config(module_name="test", lock=True)
        def test_a(config):
            if config:
                raise SystemExit
            else:
                raise SystemExit
        run_startup()
        with pytest.raises(SystemExit):
            test_a()

    @staticmethod
    def test_core_and_module():
        with pytest.raises(ValueError):
            @pass_config(core=True, module_name="test", lock=True)
            def test_a(config):
                return config
            run_startup()
            test_a()
