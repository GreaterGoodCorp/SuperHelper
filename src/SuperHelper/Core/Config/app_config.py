# This module defines two config functions, load_app_config() and save_app_config()
import logging
import typing
import json

logger = logging.getLogger("SuperHelper.Core.Config")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())

DefaultApplicationConfig: typing.Dict = {
    "CORE_CLI": {
        "DEBUG": False,
        "INSTALLED_MODULES": [
        ],
    },
    "MODULE_CONFIG": {
    },
}

ApplicationConfig: typing.Dict = dict()


def load_app_config(config_path: str) -> int:
    global ApplicationConfig
    # Initialise newest update to the config table
    ApplicationConfig = DefaultApplicationConfig
    try:
        with open(config_path) as fp:
            # De-serialise JSON to Python's dict and update
            ApplicationConfig.update(json.load(fp))
    except OSError:
        logger.exception("Config loader failed!")
    return 0


def save_app_config(config_path: str) -> int:
    global ApplicationConfig
    try:
        with open(config_path, "w") as fp:
            json.dump(ApplicationConfig, fp)
        return 0
    except OSError:
        logger.exception("Config saver failed!")
        return -1
