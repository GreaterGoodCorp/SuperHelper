# This module defines two config functions, load_app_config() and save_app_config()
import json
import logging
import sys

from SuperHelper.Core.Utils import PathLike
from SuperHelper.Core.Config import Config, DefaultCoreConfig, make_config_global, pass_config

logger = logging.getLogger("SuperHelper.Core.Config")


def load_app_config(config_path: PathLike) -> None:
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
    try:
        with open(config_path, "w") as fp:
            json.dump(config.__dict__(), fp)
    except OSError:
        logger.exception("Config saver failed!")
        sys.exit(1)
