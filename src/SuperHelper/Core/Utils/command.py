# This module defines core utilities and functionalities
import importlib.util
import logging
import pkgutil
import sys
from typing import Callable

import click

from SuperHelper.Core.Config import pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)


def load_core_commands() -> list[tuple[Callable, str]]:
    return [
        (add_modules, "core_add"),
        (remove_modules, "core_remove"),
        (list_modules, "core_list"),
    ]


@click.command("add")
@click.argument("modules", nargs=-1)
@pass_config(core=True, lock=True)
def add_modules(config: dict[str, ...], modules: list[str]) -> None:
    """Adds new modules into SuperHelper."""
    module_prefix = "SuperHelper.Modules.{}"
    for module in modules:
        module_fullname = module_prefix.format(module)
        try:
            if importlib.util.find_spec(module_fullname) is not None:
                if module_fullname not in config["INSTALLED_MODULES"]:
                    config["INSTALLED_MODULES"].append(module_fullname)
                return 0
            else:
                raise ModuleNotFoundError
        except ModuleNotFoundError:
            logger.exception(f"Module {module} not found!")
            break
    else:
        config["INSTALLED_MODULES"] = all_modules
        sys.exit(0)
    sys.exit(1)


@click.command("remove")
@click.argument("modules", nargs=-1)
@pass_config(core=True, lock=True)
def remove_modules(config: dict[str, ...], modules: list[str]) -> None:
    """Removes existing modules from SuperHelper."""
    module_prefix = "SuperHelper.Modules.{}"
    for module in modules:
        module_fullname = module_prefix.format(module)
        if module_fullname in config["INSTALLED_MODULES"]:
            config["INSTALLED_MODULES"].remove(module_fullname)
            return 0
        else:
            logger.warning(f"Module {module} not found!")
            break
    else:
        config["INSTALLED_MODULES"] = all_modules
        sys.exit(0)
    sys.exit(1)


@click.command("list")
@click.option("-a", "--all", "list_all", help="Include uninstalled modules", is_flag=True)
@pass_config(core=True, lock=False)
def list_modules(config: dict[str, ...], list_all: bool) -> None:
    """Lists installed modules"""
    import SuperHelper.Modules as Package
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
