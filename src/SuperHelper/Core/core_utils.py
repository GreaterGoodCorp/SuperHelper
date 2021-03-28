# This module defines core utilities and functionalities
import importlib.util
import pkgutil
import sys
from types import MethodType
from typing import List

import click

from SuperHelper.Core.Helper.Config import load_cli_config, save_cli_config
from SuperHelper.Core.Helper.IO import print_error, print_message


def load_core_utils() -> List[MethodType]:
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
            print_message(f"Module '{module}' installed successfully!")
        else:
            print_message(f"Module '{module}' is already installed!")
        sys.exit(0)
    else:
        print_error("Module not found!")
        print_error("Module installed unsuccessfully!")
        sys.exit(1)


@click.command("uninstall")
@click.argument("module")
def uninstall_modules(module: str):
    """Uninstall existing modules from SuperHelper."""
    config = load_cli_config()
    if module in config["INSTALLED_MODULES"]:
        config["INSTALLED_MODULES"].remove(module)
        save_cli_config(config)
        print_message("Module uninstalled successfully!")
        sys.exit(0)
    else:
        print_error("Module not found!")
        print_error("Module uninstalled unsuccessfully!")
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
            print_message(f"(Installed) {module_name}")
            count += 1
        elif list_all:
            print_message(module_name)
    if count == 0 and not list_all:
        print_message("No installed modules found!")
    sys.exit(0)
