# This module defines the config loader and saver functions.
import json
import logging
import sys

from SuperHelper.Core.Utils import PathLike
from SuperHelper.Core.Config import Config, DefaultCoreConfig, make_config_global, pass_config

logger = logging.getLogger("SuperHelper.Core.Config")
logger.setLevel(logging.DEBUG)

__all__ = [
    "load_app_config",
    "save_app_config",
]


def load_app_config(config_path: PathLike) -> None:
    """Loads the configuration of the application.

    :param config_path: The path to config file
    :type config_path: PathLike
    """
    try:
        with open(config_path) as fp:
            # De-serialise JSON to Python's dict and update
            config = Config.from_dict(json.load(fp))
            config.apply_core_patch(DefaultCoreConfig)
            make_config_global(config)
    except FileNotFoundError:
        logger.exception("Config file not found! Auto-configuring...")
        make_config_global(Config())
    except OSError:
        logger.exception("Config loader failed due to file being unreadable!")
        sys.exit(1)


@pass_config()
def save_app_config(config: Config, config_path: PathLike) -> None:
    """Saves the configuration of the application.

    :param config: The global Config instance
    :type config: Config
    :param config_path: The path to config file
    :type config_path: PathLike
    """
    try:
        with open(config_path, "w") as fp:
            json.dump(config.__dict__(), fp)
    except OSError:
        logger.exception("Config saver failed!")
        sys.exit(1)
