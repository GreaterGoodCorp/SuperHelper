# This module defines two functions, load_cli_config() and save_cli_config()
import logging
import typing

from SuperHelper.Core.Config.app_config import ApplicationConfig

logger = logging.getLogger("SuperHelper.Core.Config")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def load_cli_config() -> typing.Dict:
    return ApplicationConfig["CORE_CLI"]


def save_cli_config(config: typing.Dict) -> None:
    ApplicationConfig["CORE_CLI"] = config
