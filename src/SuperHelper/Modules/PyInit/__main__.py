import logging
import sys
import datetime
from pathlib import Path

import click
import git

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
    if path.exists():
        raise OSError("Folder already exists!")
    path.mkdir(parents=True)
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


def initialise_changelog(path: PathLike):
    try:
        with open(path / "CHANGELOG.md"):
            pass
    except OSError:
        logger.exception(f"Unable to create file {str(path / 'CHANGELOG.md')}")
        return 1
    return 0


def initialise_requirements(path: PathLike):
    try:
        with open(path / "requirements.txt") as fp:
            fp.write(BaseRequirements)
    except OSError:
        logger.exception(f"Unable to write requirements to {str(path / 'requirements.txt')}")
        return 1
    return 0


def initialise_makefile(path: PathLike):
    try:
        with open(path / "Makefile") as fp:
            fp.write(BaseMakefile)
    except OSError:
        logger.exception(f"Unable to write make recipes to {str(path / 'Makefile')}")
        return 1
    return 0


def initialise_travis(path: PathLike):
    try:
        with open(path / ".travis.yml") as fp:
            fp.write(BaseMakefile)
    except OSError:
        logger.exception(f"Unable to write TravisCI config to {str(path / '.travis.yml')}")
        return 1
    return 0


def initialise_codecov(path: PathLike):
    try:
        with open(path / ".coveragerc") as fp:
            fp.write(BaseCoverageConfig)
    except OSError:
        logger.exception(f"Unable to write coverage config to {str(path / '.coveragerc')}")
        return 1
    try:
        with open(path / "codecov.yml") as fp:
            fp.write(BaseCodecovConfig)
    except OSError:
        logger.exception(f"Unable to write CodeCov config to {str(path / 'codecov.yml')}")
        return 1
    return 0


def initialise_git(path: PathLike, name: str, email: str):
    # Initialise git repo at 'path'
    repo = git.Repo.init(path)
    # Write .gitignore
    try:
        with open(path / ".gitignore") as fp:
            fp.write(BaseGitIgnore)
    except OSError:
        logger.exception(f"Unable to write .gitignore to {str(path / '.gitignore')}")
        return 1
    # Create an Author
    p = git.Actor(name, email)
    # Make an initial commit
    index = repo.index
    index.add(["."])
    index.commit("Initial commit", author=p, committer=p)
    return 0


@click.group("py")
def main():
    """Python project tools."""
    pass


@main.command()
@click.option("--author", help="Name of the author.")
@click.option("--no-license", default=False, is_flag=True, help="Do not attach a license.")
@click.option("--no-readme", default=False, is_flag=True, help="Do not create a README file.")
@click.option("--no-changelog", default=False, is_flag=True, help="Do not create a CHANGELOG file.")
@click.option("--no-requirements", default=False, is_flag=True, help="Do not create a requirements.txt file.")
@click.option("--no-makefile", default=False, is_flag=True, help="Do not create a Makefile.")
@click.option("--no-travis", default=False, is_flag=True, help="Do not create a .travis.yml file.")
@click.option("--no-codecov", default=False, is_flag=True, help="Do not create code coverage config file.")
@click.argument("name", required=True)
def init(author, no_license, no_readme, no_changelog, no_requirements, no_makefile, no_travis, no_codecov, name):
    """Initialises a new python project."""
    try:
        path = initialise_project_folder(name)
    except OSError:
        logger.exception("Folder already exists!")
        sys.exit(1)
    if author is None:
        author = click.prompt("Enter author's name: ")
    if not no_license:
        initialise_license(path, author)
    if not no_readme:
        desc = click.prompt("Enter a short description for the project: ")
        initialise_readme(path, name, desc)
    if not no_changelog:
        initialise_changelog(path)
    if not no_requirements:
        initialise_requirements(path)
    if not no_makefile:
        initialise_makefile(path)
    if not no_travis:
        initialise_travis(path)
    if not no_codecov:
        initialise_codecov(path)
    email = click.prompt("Enter author's email: ")
    initialise_git(path, author, email)
    sys.exit(0)
