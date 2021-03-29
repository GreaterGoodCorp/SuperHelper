# This module defines two functions, load_module_config() and save_module_config()
import logging
import typing

from SuperHelper.Core.Config.app_config import ApplicationConfig

logger = logging.getLogger("SuperHelper.Core.Config")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def load_module_config(module_name: str) -> typing.Dict:
    return ApplicationConfig["MODULE_CONFIG"].get(module_name, dict())


def save_module_config(module_name: str, config: typing.Dict) -> None:
    ApplicationConfig["MODULE_CONFIG"][module_name] = config
