# This module defines two config functions, load_app_config() and save_app_config()
import logging
import typing
import json
import copy

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

ApplicationConfig: typing.Dict = copy.deepcopy(DefaultApplicationConfig)


def load_app_config(config_path: str) -> None:
    global ApplicationConfig
    try:
        with open(config_path) as fp:
            # De-serialise JSON to Python's dict and update
            ApplicationConfig.update(json.load(fp))
    except OSError:
        logger.exception("Config loader failed due to file being unreadable!")
        raise
    except json.JSONDecodeError:
        logger.exception("Config loader failed due to non-decoded values!")
        raise
    return


def save_app_config(config_path: str) -> None:
    global ApplicationConfig
    try:
        with open(config_path, "w") as fp:
            json.dump(ApplicationConfig, fp, default=lambda o: None)
    except OSError:
        logger.exception("Config saver failed!")
        raise
