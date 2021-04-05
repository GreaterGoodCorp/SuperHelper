# This module defines core utilities and functionalities
import importlib.util
import pkgutil
import typing
import logging

import click

from SuperHelper.Core.Config import Config, pass_config

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
@pass_config
def install_modules(config: Config, module: str) -> int:
    """Install new modules into SuperHelper."""
    if importlib.util.find_spec(module) is not None:
        core_cfg = config.get_core_config()
        if module not in core_cfg["INSTALLED_MODULES"]:
            core_cfg["INSTALLED_MODULES"].append(module)
        config.set_core_config(core_cfg)
        return 0
    else:
        logger.warning(f"Module {module} not found!")
        return 1


@click.command("uninstall")
@click.argument("module")
@pass_config
def uninstall_modules(config: Config, module: str):
    """Uninstall existing modules from SuperHelper."""
    core_cfg = config.get_core_config()
    if module in core_cfg["INSTALLED_MODULES"]:
        core_cfg["INSTALLED_MODULES"].remove(module)
        config.set_core_config(core_cfg)
        return 0
    else:
        logger.warning(f"Module {module} not found!")
        return 1


@click.command("list")
@click.option("-a", "--all", "list_all", help="Include uninstalled modules", is_flag=True)
@pass_config
def list_modules(config: Config, list_all: bool):
    """List installed modules"""
    core_cfg = config.get_core_config()
    import SuperHelper.Builtins as Package
    prefix = Package.__name__ + "."
    count = 0
    for _, module_name, _ in pkgutil.iter_modules(Package.__path__, prefix):
        if module_name in core_cfg["INSTALLED_MODULES"]:
            click.echo(f"(Installed) {module_name}")
            count += 1
        elif list_all:
            click.echo(module_name)
    if count == 0 and not list_all:
        click.echo("No installed modules found!")
    config.set_core_config(core_cfg)
    return 0
