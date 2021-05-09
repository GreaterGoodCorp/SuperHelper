import logging
import shutil
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
    path = Path(name).absolute().resolve()
    if path.exists():
        raise OSError("Folder already exists!")
    (path / "src" / name).mkdir(parents=True)
    open(path / "src" / name / "__init__.py", "w").close()
    return path


def initialise_license(path: PathLike, name: str):
    year = datetime.datetime.today().year
    try:
        with open(path / "LICENSE", "w") as fp:
            fp.write(BaseLicense.format(year, name))
    except OSError:
        logger.exception(f"Unable to write LICENSE to {str(path / 'LICENSE')}")
        return 1
    return 0


def initialise_readme(path: PathLike, name: str, desc: str):
    try:
        with open(path / "README.md", "w") as fp:
            fp.write(BaseLicense.format(name, desc))
    except OSError:
        logger.exception(f"Unable to write README.md to {str(path / 'README.md')}")
        return 1
    return 0


def initialise_changelog(path: PathLike):
    try:
        with open(path / "CHANGELOG.md", "w"):
            pass
    except OSError:
        logger.exception(f"Unable to create file {str(path / 'CHANGELOG.md')}")
        return 1
    return 0


def initialise_requirements(path: PathLike):
    try:
        with open(path / "requirements.txt", "w") as fp:
            fp.write(BaseRequirements)
    except OSError:
        logger.exception(f"Unable to write requirements to {str(path / 'requirements.txt')}")
        return 1
    return 0


def initialise_makefile(path: PathLike):
    try:
        with open(path / "Makefile", "w") as fp:
            fp.write(BaseMakefile)
    except OSError:
        logger.exception(f"Unable to write make recipes to {str(path / 'Makefile')}")
        return 1
    return 0


def initialise_travis(path: PathLike):
    try:
        with open(path / ".travis.yml", "w") as fp:
            fp.write(BaseTravisConfig)
    except OSError:
        logger.exception(f"Unable to write TravisCI config to {str(path / '.travis.yml')}")
        return 1
    return 0


def initialise_codecov(path: PathLike):
    try:
        with open(path / ".coveragerc", "w") as fp:
            fp.write(BaseCoverageConfig)
    except OSError:
        logger.exception(f"Unable to write coverage config to {str(path / '.coveragerc')}")
        return 1
    try:
        with open(path / "codecov.yml", "w") as fp:
            fp.write(BaseCodecovConfig)
    except OSError:
        logger.exception(f"Unable to write CodeCov config to {str(path / 'codecov.yml')}")
        return 1
    return 0


def initialise_setup(path: PathLike, name: str, author: str, email: str, desc: str):
    try:
        with open(path / "setup.py", "w") as fp:
            fp.write(BaseSetup.format(name, author, email, desc))
    except OSError:
        logger.exception(f"Unable to write setup config to {str(path / 'setup.py')}")
        return 1


def initialise_git(path: PathLike, name: str, email: str):
    # Initialise git repo at 'path'
    repo = git.Repo.init(path)
    # Write .gitignore
    try:
        with open(path / ".gitignore", "w") as fp:
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
@click.option("--email", help="Email of the author.")
@click.option("--description", help="Short description of the project.")
@click.option("--no-license", default=False, is_flag=True, help="Do not attach a license.")
@click.option("--no-readme", default=False, is_flag=True, help="Do not create a README file.")
@click.option("--no-changelog", default=False, is_flag=True, help="Do not create a CHANGELOG file.")
@click.option("--no-requirements", default=False, is_flag=True, help="Do not create a requirements.txt file.")
@click.option("--no-makefile", default=False, is_flag=True, help="Do not create a Makefile.")
@click.option("--no-ci", default=False, is_flag=True, help="Do not create CI config files.")
@click.argument("name", required=True)
def init(author, email, description, no_license, no_readme, no_changelog, no_requirements, no_ci, no_codecov, name):
    """Initialises a new python project."""

    def wrapper():
        ret = 0
        if not no_license:
            ret += initialise_license(path, author)
        if not no_readme:
            ret += initialise_readme(path, name, description)
        if not no_changelog:
            ret += initialise_changelog(path)
        if not no_requirements:
            ret += initialise_requirements(path)
        if not no_ci:
            ret += initialise_makefile(path)
            ret += initialise_travis(path)
        if not no_codecov:
            ret += initialise_codecov(path)
        return ret != 0

    try:
        path = initialise_project_folder(name)
    except OSError:
        logger.exception("Folder already exists!")
        sys.exit(1)
    if author is None:
        author = click.prompt("Enter author's name")
    if email is None:
        email = click.prompt("Enter author's email")
    if description is None:
        description = click.prompt("Enter a short description for the project")
    ret_val = wrapper()
    if ret_val:
        if path.exists():
            shutil.rmtree(path)
        sys.exit(ret_val)
    initialise_setup(path, name, author, email, description)
    initialise_git(path, author, email)
    sys.exit(0)
