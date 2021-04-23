import pathlib
import os
import sys

try:
    import click
except ImportError:
    print("Module 'click' missing! Please install it first.", file=sys.stderr)
    sys.exit(1)

__version__ = "1.1.0"
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
