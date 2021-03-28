# This module defines core utilities and functionalities
import importlib.util
import pkgutil
import sys
import types
import typing
import logging

import click

from SuperHelper.Core.Config import load_cli_config, save_cli_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def load_core_commands() -> typing.List[types.MethodType]:
    return [
        install_modules,
        uninstall_modules,
        list_modules,
    ]


@click.command("install")
@click.argument("module")
def install_modules(module: str):
    """Install new modules into SuperHelper."""
    if importlib.util.find_spec(module) is not None:
        config = load_cli_config()
        if module not in config["INSTALLED_MODULES"]:
            config["INSTALLED_MODULES"].append(module)
            save_cli_config(config)
        sys.exit(0)
    else:
        logger.warning(f"Module {module} not found!")
        sys.exit(1)


@click.command("uninstall")
@click.argument("module")
def uninstall_modules(module: str):
    """Uninstall existing modules from SuperHelper."""
    config = load_cli_config()
    if module in config["INSTALLED_MODULES"]:
        config["INSTALLED_MODULES"].remove(module)
        save_cli_config(config)
        sys.exit(0)
    else:
        logger.warning(f"Module {module} not found!")
        sys.exit(1)


@click.command("list")
@click.option("-a", "--all", "list_all", help="Include uninstalled modules", is_flag=True)
def list_modules(list_all: bool):
    """List installed modules"""
    config = load_cli_config()
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
    sys.exit(0)
