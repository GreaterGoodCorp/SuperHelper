import pathlib
import os

import click

__version__ = "1.0.0"
Version = __version__

AppName = "SuperHelper"
"""Name of the application."""
AppDir = pathlib.Path(os.getenv("SUPER_HELPER_APP_DIR", click.get_app_dir(AppName)))
"""Path to the application directory."""
AppDir.mkdir(parents=True, exist_ok=True)

__all__ = [
    "Version",
    "AppName",
    "AppDir",
]

__pdoc__ = {"SuperHelper.Tests": False}
