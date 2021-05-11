# This subpackage allows a one-off import statement of most frequently used functions for all modules
import logging

from SuperHelper import AppDir, DEBUG
from SuperHelper.Core.Utils.type_hinting import PathLike
from SuperHelper.Core.Utils.type_ensure import TypeCheck
from SuperHelper.Core.Utils.logger import get_logger
from SuperHelper.Core.Utils.bit_ops import BitOps
from SuperHelper.Core.Utils.file_ops import FileOps, FP
from SuperHelper.Core.Utils.crypto_ops import Cryptographer
from SuperHelper.Core.Config.config_class import pass_config


def initialise_module(module_name: str) -> (str, logging.Logger, PathLike):
    """Initialises a SuperHelper module on startup.

    Args:
        module_name (str): Name of the module.

    Returns:
        A tuple of (name, logger, module_dir), where name is the fully qualified name of the module (should be assigned
        to __name__), logger is a module-level logger, and module_dir is a Path instance of the path to module's own
        directory to store data.
    """
    mod_name = f"SuperHelper.Modules.{module_name}"
    mod_dir = AppDir / module_name
    mod_dir.mkdir(parents=True, exist_ok=True)
    return mod_name, get_logger(module_name), AppDir / module_name


__all__ = [
    "AppDir",
    "DEBUG",
    "TypeCheck",
    "PathLike",
    "BitOps",
    "FileOps",
    "FP",
    "Cryptographer",
    "pass_config",
    "initialise_module",
]
