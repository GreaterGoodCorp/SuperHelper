# This module defines the module loader function.
import importlib
import logging

import click

from SuperHelper.Core.Config import pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


@pass_config(core=True, lock=False)
def load_installed_modules(config: dict[str, ...]) -> list[tuple[click.Command, str]]:
    """Loads the main() method of all installed modules."""
    module_entries = []
    for module_name in config["INSTALLED_MODULES"]:
        try:
            module = importlib.import_module(module_name)
            module_entries.append((module.main, module_name))
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
        except AttributeError:
            logger.exception(f"Module '{module_name}' does not have main()!")
    return module_entries
