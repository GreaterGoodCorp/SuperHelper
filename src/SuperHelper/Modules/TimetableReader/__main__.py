import functools
import logging
import pathlib

import click

from SuperHelper import AppDir
from SuperHelper.Core import pass_config
from SuperHelper.Core.Config import Config

MODULE_NAME: str = "TimetableReader"
MODULE_DIR: pathlib.Path = AppDir / MODULE_NAME
pass_config_no_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=False)
pass_config_with_lock = functools.partial(pass_config, module_name=MODULE_NAME, lock=True)
__name__ = f"SuperHelper.Modules.{MODULE_NAME}"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@pass_config()
def patch_config(config: Config):
    """Initialise a new config dictionary.

    This function can also be used to patch the existing config.

    Returns:
        None
    """
    cfg = {

    }
    config.apply_module_patch(MODULE_NAME, cfg)
    pass


@click.group("timetable")
def main():
    """Imports timetable into calendar."""
    patch_config()


@main.command("import")
def image_import():
    """Imports timetable image file."""
