# This module defines the modules loader function.
import importlib
import logging

import click

from SuperHelper.Core.Config import pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)

__all__ = [
    "load_added_modules",
]


@pass_config(core=True, lock=False)
def load_added_modules(config: dict[str, ...]) -> list[tuple[click.Command, str]]:
    """Loads all added modules.

    :return: A list of command-name pairs to be added to Core CLI
    :rtype: list[tuple[click.Command, str]]
    """
    module_entries = []
    for module_name in config["INSTALLED_MODULES"]:
        try:
            # Attempt to import the module
            module = importlib.import_module(module_name)
            module_entries.append((module.main, module_name))
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
        except AttributeError:
            logger.exception(f"Module '{module_name}' does not have main()!")
    return module_entries
