# This module defines the entry Click CLI function
# All modules of SuperHelper should define its own group, which can imported by this module.
import os
import pathlib
import sys
from typing import NoReturn

import click

from SuperHelper import Version
from SuperHelper.Core.Utils import initialise_core_logger

APP_NAME = "SuperHelper"
APP_DIR = click.get_app_dir(APP_NAME)
pathlib.Path(APP_DIR).mkdir(parents=True, exist_ok=True)

CONFIG_FILENAME = f"{APP_NAME}.cfg"
DEFAULT_CONFIG_PATH = pathlib.Path(click.get_app_dir("SuperHelper")) / CONFIG_FILENAME
CONFIG_PATH = os.getenv("SUPER_HELPER_CONFIG_PATH", DEFAULT_CONFIG_PATH)

LOGGING_FILENAME = f"{APP_NAME}.log"
DEFAULT_LOGGING_PATH = pathlib.Path(click.get_app_dir("SuperHelper")) / LOGGING_FILENAME
LOGGING_PATH = os.getenv("SUPER_HELPER_LOGGING_PATH", DEFAULT_LOGGING_PATH)


def validate_no_win32() -> None:
    """This function asserts that the platform is not 'win32'."""
    assert sys.platform != "win32", "This application is not configured to run on Windows."


# Program entry point
@click.group()
@click.version_option(Version)
def cli() -> int:
    pass


# Console entry call
def main_entry() -> NoReturn:
    validate_no_win32()
    # Load core logger
    logger = initialise_core_logger(LOGGING_PATH)
    try:
        # Load application config
        from SuperHelper.Core.Config import load_app_config, save_app_config
        load_app_config(CONFIG_PATH)
    except RuntimeError:
        sys.exit(1)
    # Load core utilities and functionalities
    from SuperHelper.Core.Utils import load_core_commands
    for core_module in load_core_commands():
        try:
            cli.add_command(core_module[0])
        except Exception or BaseException:
            logger.exception(f"Unable to load core module {core_module[1]}")
        else:
            logger.debug(f"Loaded core module {core_module[1]}")
    # Load installed modules
    from SuperHelper.Core.Utils import load_installed_modules
    for module in load_installed_modules():
        try:
            cli.add_command(module[0])
        except Exception or BaseException:
            logger.exception(f"Unable to load module {module[1]}")
        else:
            logger.debug(f"Loaded module {module[1]}")
    try:
        # Print all messages before executing CLI
        sys.stdout.flush()
        sys.stderr.flush()
        # Execute CLI
        sys.exit(cli())
    except SystemExit:
        # Save application config
        save_app_config(CONFIG_PATH)
        raise


if __name__ == '__main__':
    sys.argv[0] = "SuperHelper"
    main_entry()
