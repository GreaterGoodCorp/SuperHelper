# This module defines two functions, load_cli_config() and save_cli_config()
import logging
import typing

from SuperHelper.Core.Config.app_config import ApplicationConfig

logger = logging.getLogger("SuperHelper.Core.Config")


def load_cli_config() -> typing.Dict:
    try:
        return ApplicationConfig["CORE_CLI"]
    except KeyError:
        logger.exception("CORE_CLI not found!")
        logger.debug(ApplicationConfig)


def save_cli_config(config: typing.Dict) -> None:
    ApplicationConfig["CORE_CLI"] = config
