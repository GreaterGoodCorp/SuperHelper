# This module defines two config functions, load_app_config() and save_app_config()
import json
import logging

from SuperHelper.Core.Config import Config, DefaultCoreConfig, make_config_global, pass_config

logger = logging.getLogger("SuperHelper.Core.Config")


def load_app_config(config_path: str) -> None:
    try:
        with open(config_path) as fp:
            # De-serialise JSON to Python's dict and update
            config: Config = json.load(fp, object_hook=Config.json_decode_hook)
            config.apply_core_patch(DefaultCoreConfig)
            make_config_global(config)
    except FileNotFoundError:
        logger.exception("Config file not found! Auto-configuring...")
        make_config_global(Config())
    except OSError:
        logger.exception("Config loader failed due to file being unreadable!")
        raise RuntimeError


@pass_config()
def save_app_config(config: Config, config_path: str) -> None:
    try:
        with open(config_path, "w") as fp:
            json.dump(config.__dict__(), fp)
    except OSError:
        logger.exception("Config saver failed!")
        raise RuntimeError
