# This module defines the module loader function.
import importlib
import logging
import typing

import click

from SuperHelper.Core.Config import Config, pass_config

logger = logging.getLogger("SuperHelper.Core.Utils")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


@pass_config
def load_installed_modules(config: Config) -> typing.List[typing.Tuple[click.Command, str]]:
    """Loads the main() method of all installed modules."""
    module_entries = []
    cli_config = config.get_core_config()
    for module_name in cli_config["INSTALLED_MODULES"]:
        try:
            module = importlib.import_module(module_name)
            module_entries.append((module.main, module_name))
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
        except AttributeError:
            logger.exception(f"Module '{module_name}' does not have main()!")
    config.set_core_config(cli_config)
    return module_entries
