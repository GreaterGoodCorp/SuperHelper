# This module contains the Config class, which contains the application configuration.
from __future__ import annotations

import copy
import logging
from functools import wraps
from typing import Callable

logger: logging.Logger = logging.getLogger("SuperHelper.Core.Config")

DefaultCoreConfig: dict[str, ...] = {
    "DEBUG": False,
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
    """
    An internal metaclass, only used for `Config`.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logger.debug("Initialising config")
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        logger.debug("Retrieving config singleton")
        return cls._instances[cls]


class Config(metaclass=Singleton):
    """
    The configuration of the application.
    """
    _core_lock: bool = False

    def __init__(self, core: dict[str, ...] = None, modules: dict[str, dict[str, ...]] = None) -> None:
        self._Core: dict[str, ...] = core if core is not None else DefaultCoreConfig
        self._Modules: dict[str, ...] = modules if modules is not None else dict()
        return

    def get_core_config(self, lock: bool = True) -> dict[str, ...]:
        """Gets the configuration of Core CLI.

        This function is intended for internal use only, used for the decorator `pass_config`.
        """
        if Config._core_lock:
            raise RuntimeError("Core config is already retrieved!")
        if lock:
            # Lock core config
            Config._core_lock = True
        return copy.deepcopy(self._Core)

    def set_core_config(self, config: dict[str, ...]) -> None:
        """Sets the configuration of Core CLI.

        This function is intended for internal use only, used for the decorator `pass_config`.
        """
        # Release lock core config
        if not Config._core_lock:
            raise RuntimeError("No lock was acquired! Write access is disabled!")
        Config._core_lock = False
        self._Core = copy.deepcopy(config)
        return

    def apply_core_patch(self, config: dict[str, ...]) -> None:
        """Applies a new patch to core configuration.

        This function should only be used by Core CLI.

        :param config: The patch of the configuration.
        :type config: dict[str, ...]
        """
        try:
            # Secure core config
            core_config = self.get_core_config()
            # Apply patch
            config = copy.deepcopy(config)
            config.update(core_config)
            # Release core config
            self.set_core_config(core_config)
        except RuntimeError:
            logger.exception("Cannot secure core config")
            raise

    def get_module_config(self, module_name: str, lock: bool = True) -> dict[str, ...]:
        """Get the module configuration

        This function is intended for internal use only, used for the decorator `pass_config`.
        """
        lock_name = f"{module_name}_lock"
        assert not getattr(self, lock_name, False), f"{module_name} config is already retrieved!"
        if lock:
            # Lock module config
            setattr(self, lock_name, True)
        if module_name not in self._Modules.keys():
            # Make placeholder
            self._Modules[module_name] = dict()
        return copy.deepcopy(self._Modules[module_name])

    def set_module_config(self, module_name: str, config: dict[str, ...]) -> None:
        """Set the module configuration.

        This function is intended for internal use only, used for the decorator `pass_config`.
        """
        # Release lock module config
        lock_name = f"{module_name}_lock"
        is_locked = not getattr(self, lock_name, False)
        is_set = module_name in config.keys()
        if is_locked and not is_set:
            raise RuntimeError("No lock was acquired! Write access is disabled!")
        setattr(self, lock_name, False)
        self._Modules[module_name] = copy.deepcopy(config)
        return

    def apply_module_patch(self, module_name: str, config: dict[str, ...]) -> None:
        """Applies a new patch to the module configuration

        :param module_name: The name of the module to apply patch to
        :type module_name: str
        :param config: The patch of the configuration
        :type config: dict[str, ...]
        """
        try:
            # Secure module config
            module_config = self.get_module_config(module_name)
            # Apply patch
            config = copy.deepcopy(config)
            config.update(module_config)
            # Release module config
            self.set_module_config(module_name, config)
        except RuntimeError:
            logger.exception(f"Cannot secure module '{module_name}' config")
            raise

    def __dict__(self) -> dict[str, dict[str, ...]]:
        return {
            "Core": self._Core,
            "Modules": self._Modules,
        }

    @staticmethod
    def from_dict(config: dict[str]) -> Config:
        """Deserializes a JSON dictionary to Config object.

        This function is intended for internal use only.
        """
        if "Core" in config.keys() and "Modules" in config.keys():
            return Config(core=config["Core"], modules=config["Modules"])


# The container for the global configuration of the application
global_config: Config


def make_config_global(cfg: Config) -> None:
    """Makes the configuration global.

    This function is intended for internal use only.
    """
    global global_config
    global_config = cfg


def pass_config(core: bool = None, module_name: str = None, lock: bool = False, param_name: str = "config") -> Callable:
    """Passes the requested config to decorated functions.

    :param core: Whether to request core config
    :type core: bool
    :param module_name: The name of the module
    :type module_name: str
    :param lock: Whether to lock the config, i.e allow writing to the config
    :type lock: bool
    :param param_name: The name of the parameter that the config will be passed as
    :type param_name: str
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
