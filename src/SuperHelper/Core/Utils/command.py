# This module defines core utilities and functionalities
import importlib.util
import logging
import pkgutil
import typing

import click

from SuperHelper.Core.Config import pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def load_core_commands() -> typing.List[typing.Tuple[click.Command, str]]:
    return [
        (install_modules, "core_install"),
        (uninstall_modules, "core_uninstall"),
        (list_modules, "core_list"),
    ]


@click.command("install")
@click.argument("module")
@pass_config(core=True, lock=True)
def install_modules(config: dict[str, ...], module: str) -> int:
    """Install new modules into SuperHelper."""
    if importlib.util.find_spec(module) is not None:
        if module not in config["INSTALLED_MODULES"]:
            config["INSTALLED_MODULES"].append(module)
        return 0
    else:
        logger.warning(f"Module {module} not found!")
        return 1


@click.command("uninstall")
@click.argument("module")
@pass_config(core=True, lock=True)
def uninstall_modules(config: dict[str, ...], module: str):
    """Uninstall existing modules from SuperHelper."""
    if module in config["INSTALLED_MODULES"]:
        config["INSTALLED_MODULES"].remove(module)
        return 0
    else:
        logger.warning(f"Module {module} not found!")
        return 1


@click.command("list")
@click.option("-a", "--all", "list_all", help="Include uninstalled modules", is_flag=True)
@pass_config(core=True, lock=False)
def list_modules(config: dict[str, ...], list_all: bool):
    """List installed modules"""
    import SuperHelper.Builtins as Package
    prefix = Package.__name__ + "."
    count = 0
    for _, module_name, _ in pkgutil.iter_modules(Package.__path__, prefix):
        if module_name in config["INSTALLED_MODULES"]:
            click.echo(f"(Installed) {module_name}")
            count += 1
        elif list_all:
            click.echo(module_name)
    if count == 0 and not list_all:
        click.echo("No installed modules found!")
    return 0
