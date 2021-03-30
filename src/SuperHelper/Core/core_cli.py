# This module defines the entry Click CLI function
# All modules of SuperHelper should define its own group, which can imported by this module.
import os
import pathlib
import sys

import click

from SuperHelper import Version

CONFIG_FILENAME = ".super_helper"
DEFAULT_CONFIG_PATH = pathlib.Path.home() / CONFIG_FILENAME
CONFIG_PATH = os.getenv("SUPER_HELPER_CONFIG_PATH", DEFAULT_CONFIG_PATH)


# Program entry point
@click.group()
@click.version_option(Version)
def cli():
    pass


# Console entry call
def main_entry():
    # Load application config
    from SuperHelper.Core.Config import load_app_config, save_app_config
    load_app_config(CONFIG_PATH)
    # Load core logger
    logger = initialise_core_logger()
    # Load core utilities and functionalities
    from SuperHelper.Core.Utils import load_core_commands
    for core_module in load_core_commands():
        try:
            cli.add_command(core_module)
        except Exception or BaseException:
            logger.exception(f"Unable to load core module {core_module.__qualname__}")
        else:
            logger.debug(f"Loaded core module {core_module.__qualname__}")
    # Load installed modules
    from SuperHelper.Core.Utils import load_installed_modules
    for module in load_installed_modules():
        try:
            cli.add_command(module)
        except Exception or BaseException:
            logger.exception(f"Unable to load module {core_module.__qualname__}")
        else:
            logger.debug(f"Loaded module {core_module.__qualname__}")
    try:
        # Execute CLI
        sys.exit(cli())
    except SystemExit:
        # Save application config
        save_app_config(CONFIG_PATH)
        raise


if __name__ == '__main__':
    sys.argv[0] = "SuperHelper"
    main_entry()
