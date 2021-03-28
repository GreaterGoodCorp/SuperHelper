# This module defines the module loader function.
import importlib
import logging
from types import MethodType
from typing import List

from SuperHelper.Core.Helper import load_cli_config
from SuperHelper.Core.Helper.IO import print_error

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler)


def load_installed_modules() -> List[MethodType]:
    module_entries = []
    cli_config = load_cli_config()
    for module_name in cli_config["INSTALLED_MODULES"]:
        try:
            module_entries.append(importlib.import_module(module_name).main)
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
            print_error(f"Cannot import module '{module_name}'!")
    return module_entries
