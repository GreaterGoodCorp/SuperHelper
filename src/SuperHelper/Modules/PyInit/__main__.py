import logging
import sys
from pathlib import Path
from subprocess import Popen

import click

from SuperHelper import AppDir
from SuperHelper.Core.Utils import PathLike
from SuperHelper.Modules.PyInit.__meta__ import *

ModuleName = "PyInit"
__name__ = f"SuperHelper.Modules.{ModuleName}"
ModuleDir = AppDir / ModuleName
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def initialise_project_folder(name: str) -> PathLike:
    return Path(name).absolute()


def initialise_git(path: PathLike):
    # Get CWD
    cwd = Path(path).absolute()
    cwd.mkdir(exist_ok=True, parents=True)
    # Initialise git repo at 'path'
    Popen(["git", "init", str(cwd)], stdout=None)
    #
    pass


@click.group("py")
def main():
    """Python project tools."""
    pass


@main.command()
@click.argument("name", required=True)
def init(name):
    """Initialises a new python project."""
    path = initialise_project_folder(name)
    initialise_git(path)
    sys.exit(0)
