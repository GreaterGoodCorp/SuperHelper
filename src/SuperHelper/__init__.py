import pathlib
import os
import sys

try:
    import click
except ImportError:
    print("Module 'click' missing! Please install it first.", file=sys.stderr)
    sys.exit(1)


def set_debug_mode(mode: bool = False):
    global DEBUG
    DEBUG = mode


__version__ = "1.1.0"
Version = __version__

AppName = "SuperHelper"
"""Name of the application."""
AppDir = pathlib.Path(os.getenv("SUPER_HELPER_APP_DIR", click.get_app_dir(AppName)))
"""Path to the application directory."""
AppDir.mkdir(parents=True, exist_ok=True)
DEBUG = False
"""Whether the debug mode is on."""

__all__ = [
    "Version",
    "AppName",
    "AppDir",
    "set_debug_mode",
    "DEBUG",
]

__pdoc__ = {"SuperHelper.Tests": False}
