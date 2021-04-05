# This module defines two config functions, load_app_config() and save_app_config()
import json
import logging

from SuperHelper.Core.Config import Config

logger = logging.getLogger("SuperHelper.Core.Config")

DefaultCoreConfig: dict[str, ...] = {
    "DEBUG": "False",
    "INSTALLED_MODULES": [
    ],
}


def load_app_config(config_path: str) -> Config:
    try:
        with open(config_path) as fp:
            # De-serialise JSON to Python's dict and update
            config: Config = json.load(fp, object_hook=Config.json_decode_hook)
            config.apply_core_patch(DefaultCoreConfig)
            return config
    except FileNotFoundError:
        logger.exception("Config file not found! Please run 'helper configure' first!")
        raise RuntimeError
    except OSError:
        logger.exception("Config loader failed due to file being unreadable!")
        raise RuntimeError


def save_app_config(config_path: str, config: Config) -> None:
    try:
        with open(config_path, "w") as fp:
            json.dump(config, fp)
    except OSError:
        logger.exception("Config saver failed!")
        raise
