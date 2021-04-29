# This module contains the Config class, which contains the application configuration.
from __future__ import annotations

import copy
import logging
from functools import wraps
from typing import Callable

from SuperHelper.Core.Utils import TypeCheck

logger: logging.Logger = logging.getLogger("SuperHelper.Core.Config")

DefaultCoreConfig: dict[str, ...] = {
    "INSTALLED_MODULES": [
    ],
}

__all__ = [
    "DefaultCoreConfig",
    "Config",
    "make_config_global",
    "pass_config",
]


class Singleton(type):
    """An internal metaclass, only used for `Config`."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logger.debug("Initialising config")
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    """The configuration of the application."""
    _core_lock: bool = False

    def __init__(self, core: dict[str, ...] = None, modules: dict[str, dict[str, ...]] = None) -> None:
        self._Core: dict[str, ...] = core if core is not None else DefaultCoreConfig
        self._Modules: dict[str, ...] = modules if modules is not None else dict()
        return

    def get_core_config(self, lock: bool = True) -> dict[str, ...]:
        """Gets the configuration of Core CLI.

        This function is intended for internal use only, used for the decorator `pass_config`.

        Args:
            lock (bool): Whether to lock the config or not.

        Returns:
            A dictionary mapping keys to corresponding values of the core config. Each entry is represented by a
            key-value pair of the dictionary. For example:

            ```
            {"DEBUG": ..., "INSTALLED_MODULES": [...]}
            ```

            The keys are always strings, and the values can be of any JSON-serializable type.

        Raises:
            RuntimeError: The core config is locked by another call.
        """
        TypeCheck.ensure_bool(lock, "lock")
        if Config._core_lock:
            raise RuntimeError("Core config is locked, read access is not allowed!")
        if lock:
            # Lock core config
            Config._core_lock = True
        return copy.deepcopy(self._Core)

    def set_core_config(self, config: dict[str, ...]) -> None:
        """Sets the configuration of Core CLI.

        This function is intended for internal use only, used for the decorator `pass_config`.

        Args:
            config (dict[str, ...]): A dictionary with string keys of the core configuration.

        Returns:
            None

        Raises:
            RuntimeError: The last retrieval of the core config was not locked, hence it is read-only.
        """
        # Release lock core config
        if not Config._core_lock:
            raise RuntimeError("Core config is unlocked, write access is not allowed!")
        Config._core_lock = False
        self._Core = copy.deepcopy(config)
        return

    def apply_core_patch(self, config: dict[str, ...]) -> None:
        """Applies a new patch to core configuration.

        This function should only be used by Core CLI.

        Args:
            config (dict[str, ...]): The patch of the configuration.

        Returns:
            None

        Raises:
            RuntimeError: An error has occurred in `self.get_core_config()`
        """
        # Secure core config
        core_config = self.get_core_config()
        # Apply patch
        config = copy.deepcopy(config)
        config.update(core_config)
        # Release core config
        self.set_core_config(core_config)

    def get_module_config(self, module_name: str, lock: bool = True) -> dict[str, ...]:
        """Gets the configuration of the specified module.

        This function is intended for internal use only, used for the decorator `pass_config`.

        Args:
            module_name (str): The name of the module that the config belongs to.
            lock (bool): Whether to lock the config or not.

        Returns:
            A dictionary mapping keys to corresponding values of the module config. Each entry is represented by a
            key-value pair of the dictionary. For example:

            ```
            {"DEBUG": ..., "INSTALLED_MODULES": [...]}
            ```

            The keys are always strings, and the values can be of any JSON-serializable type.

        Raises:
            RuntimeError: The module config is locked by another call.
        """
        lock_name = f"{module_name}_lock"
        if getattr(self, lock_name, False):
            raise RuntimeError(f"'{module_name}' config is locked, read access is not allowed!")
        if lock:
            # Lock module config
            setattr(self, lock_name, True)
        if module_name not in self._Modules.keys():
            # Make placeholder
            self._Modules[module_name] = dict()
        return copy.deepcopy(self._Modules[module_name])

    def set_module_config(self, module_name: str, config: dict[str, ...]) -> None:
        """Sets the module configuration.

        This function is intended for internal use only, used for the decorator `pass_config`.

        Args:
            module_name (str): The name of the module that the config belongs to.
            config (dict[str, ...]): A dictionary with string keys of the core configuration.

        Returns:
            None

        Raises:
            RuntimeError: The last retrieval of the module config was not locked, hence it is read-only.
        """
        # Release lock module config
        lock_name = f"{module_name}_lock"
        is_locked = not getattr(self, lock_name, False)
        is_set = module_name in config.keys()
        if is_locked and not is_set:
            raise RuntimeError(f"'{module_name}' config is unlocked, write access is not allowed!")
        setattr(self, lock_name, False)
        self._Modules[module_name] = copy.deepcopy(config)
        return

    def apply_module_patch(self, module_name: str, config: dict[str, ...]) -> None:
        """Applies a new patch to the module configuration.

        Args:
            module_name (str): The name of the module to apply patch to.
            config (dict[str, ...]): The patch of the configuration.

        Returns:
            None
        """
        # Secure module config
        module_config = self.get_module_config(module_name)
        # Apply patch
        config = copy.deepcopy(config)
        config.update(module_config)
        # Release module config
        self.set_module_config(module_name, config)

    def __dict__(self) -> dict[str, dict[str, ...]]:
        return {
            "Core": self._Core,
            "Modules": self._Modules,
        }

    @staticmethod
    def from_dict(config: dict[str]) -> Config:
        if "Core" in config.keys() and "Modules" in config.keys():
            return Config(core=config["Core"], modules=config["Modules"])


# The container for the global configuration of the application
global_config: Config


def make_config_global(cfg: Config) -> None:
    """Makes the configuration global.

    Args:
        cfg (Config): The `Config` instance.

    Returns:
        None
    """
    global global_config
    global_config = cfg


def pass_config(core: bool = None, module_name: str = None, lock: bool = False, param_name: str = "config") -> Callable:
    """Passes the requested config to decorated functions.

    The wrapped function will receive the config (as requested). When the function returns (or raises SystemExit), this
    decorator will capture that signal, save the config (if locked) before returning (or re-raising SystemExit).

    Args:
        core (bool): Whether to request core config.
        module_name (str): The name of the module.
        lock (bool): Whether to lock the config, i.e allow writing to the config.
        param_name (str): The name of the parameter that the config will be passed as.

    Returns:
        A Callable instance (the decorated function).

    Raises:
        SystemExit: Re-raises the `SystemExit()` raised by the wrapped function.
        ValueError: Both `core` and `module_name` are specified.
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> ...:
            if core is None and module_name is None:
                return f(global_config, *args, **kwargs)
            elif core is not None and module_name is None:
                if lock:
                    config = global_config.get_core_config(lock=True)
                    kwargs[param_name] = config
                    try:
                        ret_val = f(*args, **kwargs)
                        global_config.set_core_config(config)
                        return ret_val
                    except SystemExit:
                        global_config.set_core_config(config)
                        raise
                else:
                    kwargs[param_name] = global_config.get_core_config(lock=False)
                    return f(*args, **kwargs)
            elif core is None and module_name is not None:
                if lock:
                    config = global_config.get_module_config(module_name, lock=True)
                    kwargs[param_name] = config
                    try:
                        ret_val = f(*args, **kwargs)
                        global_config.set_module_config(module_name, config)
                        return ret_val
                    except SystemExit:
                        global_config.set_module_config(module_name, config)
                        raise
                else:
                    kwargs[param_name] = global_config.get_module_config(module_name, lock=lock)
                    return f(*args, **kwargs)
            else:
                raise ValueError("Core and module name cannot be enabled at the same time!")

        return wrapper

    return decorator
