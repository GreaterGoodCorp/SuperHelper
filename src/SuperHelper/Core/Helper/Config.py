# This module defines the config loader functions, which can be used by all modules
import logging
import os
import re
from json import load, dump
from pathlib import Path
from typing import Dict

from SuperHelper.Core.Helper.IO import print_error

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())

DEFAULT_CONFIG_PATH = Path.home() / ".super_helper"

# Retrieve environment variable
CONFIG_PATH = os.getenv("SUPER_HELPER_CONFIG_PATH", DEFAULT_CONFIG_PATH)

_APP_CONFIG: Dict


def get_subpackage_name(name: str) -> str:
    return ".".join(name.split(".")[:-1])


def initialise_default_app_config() -> Dict:
    return {
        "CORE_CLI": {
            "DEBUG": False,
            "INSTALLED_MODULES": [
                "SuperHelper.Builtins.FocusEnabler",
            ],
        },
        "MODULE_CONFIG": {
        },
    }


def load_app_config() -> int:
    global _APP_CONFIG
    # Try-catch the file opening
    try:
        with open(CONFIG_PATH) as fp:
            # De-serialise JSON to Python's dict
            _APP_CONFIG = load(fp)
    except OSError:
        logger.exception("Config loader failed!")
        print_error("Unable to load config file! Making one...")
        _APP_CONFIG = initialise_default_app_config()
    return 0


def save_app_config() -> int:
    global _APP_CONFIG
    try:
        with open(CONFIG_PATH, "w") as fp:
            dump(_APP_CONFIG, fp)
        return 0
    except OSError:
        logger.exception("Config saver failed!")
        print_error("Unable to save config file!")
        return -1


def load_cli_config() -> Dict:
    return _APP_CONFIG["CORE_CLI"]


def save_cli_config(config: Dict) -> None:
    _APP_CONFIG["CORE_CLI"] = config


def load_module_config(module_name: str) -> Dict:
    try:
        if re.match(r"^[_a-zA-Z][a-zA-Z_0-9]{0,63}(\.[_a-zA-Z][a-zA-Z_0-9]{0,63})*$", module_name):
            module_name = get_subpackage_name(module_name)
        return _APP_CONFIG["MODULE_CONFIG"][module_name]
    except KeyError:
        return dict()


def save_module_config(module_name: str, config: Dict) -> None:
    if re.match(r"^[_a-zA-Z][a-zA-Z_0-9]{0,63}(\.[_a-zA-Z][a-zA-Z_0-9]{0,63})*$", module_name):
        module_name = get_subpackage_name(module_name)
    _APP_CONFIG["MODULE_CONFIG"][module_name] = config
