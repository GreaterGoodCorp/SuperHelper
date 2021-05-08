import logging
import sys
import datetime
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
    path = Path(name).absolute()
    path.mkdir(exist_ok=True, parents=True)
    return path


def initialise_license(path: PathLike, name: str):
    year = datetime.datetime.today().year
    try:
        with open(path / "LICENSE") as fp:
            fp.write(BaseLicense.format(year, name))
    except OSError:
        logger.exception(f"Unable to write LICENSE to {str(path / 'LICENSE')}")
        return 1
    return 0


def initialise_readme(path: PathLike, name: str, desc: str):
    try:
        with open(path / "README.md") as fp:
            fp.write(BaseLicense.format(name, desc))
    except OSError:
        logger.exception(f"Unable to write README.md to {str(path / 'README.md')}")
        return 1
    return 0


def initialise_git(path: PathLike):
    # Initialise git repo at 'path'
    p = Popen(["git", "init", str(path)], stdout=None)
    if p.returncode != 0:
        logger.error("Unable to initialise git repo\n" + p.stderr.read().decode("utf-8"))
        return p.returncode
    # Write .gitignore
    try:
        with open(path / ".gitignore") as fp:
            fp.write(BaseGitIgnore)
    except OSError:
        logger.exception(f"Unable to write .gitignore to {str(path / '.gitignore')}")
        return 1
    return 0


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
