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

    Returns:
        A list of a 2-tuple elements, where the first index is the `click.command` object, and the second index is the
        technical name of the command. For example:

        ```
        [(main, "main"), ...]
        ```

        The first index can be added to a `click.group`, i.e the `cli` function.
    """
    module_entries = []
    for module_name in config["INSTALLED_MODULES"]:
        try:
            # Attempt to import the module
            module = importlib.import_module(module_name)
            module_entries.append((module.main, module_name))
        except ImportError:
            logger.exception(f"Unable to import module '{module_name}'!")
        except AttributeError:
            logger.exception(f"Unable to look up 'main()' for module '{module_name}'")
    return module_entries
