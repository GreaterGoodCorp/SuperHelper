# This module defines the entry Click CLI function
# All modules of SuperHelper should define its own group, which can imported by this module.
import logging
import os
import pathlib
import platform
import sys
from typing import NoReturn

import click

from SuperHelper import Version
from SuperHelper.Core.Utils import initialise_core_logger

APP_NAME = "SuperHelper"
APP_DIR = pathlib.Path(os.getenv("SUPER_HELPER_APP_DIR", click.get_app_dir(APP_NAME)))
APP_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILENAME = f"{APP_NAME}.cfg"
CONFIG_PATH = APP_DIR / CONFIG_FILENAME

LOGGING_FILENAME = f"{APP_NAME}.log"
LOGGING_PATH = APP_DIR / LOGGING_FILENAME

version_message = f"%(prog)s-%(version)s {platform.platform(terse=True)} Python-{platform.python_version()}"
logger: logging.Logger


# Program entry point
@click.group()
@click.version_option(Version, prog_name=APP_NAME, message=version_message)
def cli() -> None:
    pass


def validate_no_win32() -> None:
    """This function asserts that the platform is not 'win32'."""
    try:
        assert sys.platform != "win32"
    except AssertionError:
        logger.exception("This application cannot run on Windows!")
        sys.exit(1)


def make_logger_global():
    global logger
    logger = initialise_core_logger(LOGGING_PATH)


def load_config():
    from SuperHelper.Core.Config import load_app_config
    load_app_config(CONFIG_PATH)


def save_config():
    from SuperHelper.Core.Config import save_app_config
    save_app_config(CONFIG_PATH)


def load_core_commands():
    from SuperHelper.Core.Utils import load_core_commands
    for core_module in load_core_commands():
        try:
            cli.add_command(core_module[0])
        except Exception or BaseException:
            logger.exception(f"Unable to load core module {core_module[1]}")
            sys.exit(1)
        else:
            logger.debug(f"Loaded core module {core_module[1]}")


def load_added_modules():
    from SuperHelper.Core.Utils import load_installed_modules
    for module in load_installed_modules():
        try:
            cli.add_command(module[0])
        except Exception or BaseException:
            logger.exception(f"Unable to load module {module[1]}")
        else:
            logger.debug(f"Loaded module {module[1]}")


def run_startup():
    # Load core logger
    make_logger_global()
    # Validate platform
    validate_no_win32()
    # Load config
    load_config()
    # Load core utilities and functionalities
    load_core_commands()
    # Load installed modules
    load_added_modules()


# Console entry call
def main_entry() -> NoReturn:
    # Run startup setting
    run_startup()
    try:
        # Print all messages before executing CLI
        sys.stdout.flush()
        sys.stderr.flush()
        # Execute CLI
        sys.exit(cli())
    except SystemExit:
        # Save application config
        save_config()
        raise


__all__ = [
    "run_startup",
    "load_config",
    "save_config",
    "main_entry",
    "cli",
]

if __name__ == '__main__':
    sys.argv[0] = "SuperHelper"
    main_entry()
