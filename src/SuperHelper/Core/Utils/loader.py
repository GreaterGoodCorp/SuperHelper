# This module defines the module loader function.
import importlib
import logging
import types
import typing

from SuperHelper.Core.Config import load_cli_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def load_installed_modules() -> typing.List[types.MethodType]:
    """Loads the main() method of all installed modules."""
    module_entries = []
    cli_config = load_cli_config()
    for module_name in cli_config["INSTALLED_MODULES"]:
        try:
            module = importlib.import_module(module_name)
            module_entries.append(module.main)
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
        except AttributeError:
            logger.exception(f"Module '{module_name}' does not have main()!")
    return module_entries
