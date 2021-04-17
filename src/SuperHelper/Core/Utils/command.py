# This module defines Core CLI utilities and functionalities
import copy
import importlib.util
import logging
import pkgutil
import sys
from typing import Callable

import click

from SuperHelper.Core.Config import pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)

__all__ = [
    "load_core_commands",
]


def load_core_commands() -> list[tuple[Callable, str]]:
    """Returns the Core CLI commands.

    :return: A list of command-name pairs to be added to Core CLI
    :rtype: list[tuple[Callable, str]]
    """
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
    # Deep-copy the list to avoid modifying it in place
    all_modules = copy.deepcopy(config["INSTALLED_MODULES"])
    for module in modules:
        # Append the module prefix to module name
        module_fullname = module_prefix.format(module)
        try:
            # Check if the module is found
            # If the module is installed, it should be located as follows:
            # SuperHelper.Modules.<ModuleName>
            # Otherwise, it is not found (or not installed)
            if importlib.util.find_spec(module_fullname) is not None:
                if module_fullname not in config["INSTALLED_MODULES"]:
                    all_modules.append(module_fullname)
            else:
                raise ModuleNotFoundError
        except ModuleNotFoundError:
            logger.exception(f"Module {module} not found!\nReverting...")
            break
    else:
        # Save the config if and only if there are no errors and exit with 0.
        config["INSTALLED_MODULES"] = all_modules
        sys.exit(0)
    # Otherwise, if there are errors, exit with a non-zero code, i.e. 1.
    sys.exit(1)


@click.command("remove")
@click.argument("modules", nargs=-1)
@pass_config(core=True, lock=True)
def remove_modules(config: dict[str, ...], modules: list[str]) -> None:
    """Removes existing modules from SuperHelper."""
    module_prefix = "SuperHelper.Modules.{}"
    # Deep-copy the list to avoid modifying it in place
    all_modules = copy.deepcopy(config["INSTALLED_MODULES"])
    for module in modules:
        # Append the module prefix to module name
        module_fullname = module_prefix.format(module)
        # Check if the module is already added, if so, then remove
        if module_fullname in all_modules:
            all_modules.remove(module_fullname)
        # Check if there are repeated modules, if so, ignore the repeated one
        elif module_fullname in config["INSTALLED_MODULES"]:
            continue
        # If the module is not found, i.e. not added, cancel the operations
        else:
            logger.warning(f"Module {module} not found!\nReverting...")
            break
    else:
        # Save the config if and only if there are no errors and exit with 0
        config["INSTALLED_MODULES"] = all_modules
        sys.exit(0)
    # Otherwise, if there are errors, exit with a non-zero code, i.e. 1
    sys.exit(1)


@click.command("list")
@click.option("-a", "--all", "list_all", help="Include uninstalled modules", is_flag=True)
@pass_config(core=True, lock=False)
def list_modules(config: dict[str, ...], list_all: bool) -> None:
    """Lists installed modules"""
    import SuperHelper.Modules as Package
    prefix = Package.__name__ + "."
    count = 0
    # Iterate over all installed modules found in SuperHelper.Modules
    for _, module_name, _ in pkgutil.iter_modules(Package.__path__, prefix):
        # If the module is added, print it as installed
        short_module_name = module_name.split(".")[-1]
        if module_name in config["INSTALLED_MODULES"]:
            click.echo(f"(Installed) {short_module_name}")
            count += 1
        elif list_all:
            # Otherwise, if --all is specified, print it as not installed
            click.echo(short_module_name)
    # If --all is not specified and there are no installed modules, also report to the user
    if count == 0 and not list_all:
        click.echo("No installed modules found!")
    # Then exit with 0
    sys.exit(0)
