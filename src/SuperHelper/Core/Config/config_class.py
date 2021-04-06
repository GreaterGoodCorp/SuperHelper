import copy
import logging
from functools import wraps
from typing import Callable

logger: logging.Logger = logging.getLogger("SuperHelper.Core.Config")

DefaultCoreConfig: dict[str, ...] = {
    "DEBUG": "False",
    "INSTALLED_MODULES": [
    ],
}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            logger.debug("Initialising config")
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        logger.debug("Retrieving config singleton")
        return cls._instances[cls]


class Config(metaclass=Singleton):
    _core_lock: bool = False

    def __init__(self, core: dict[str, ...] = None, modules: dict[str, dict[str, ...]] = None) -> None:
        self._Core: dict[str, ...] = core if core is not None else DefaultCoreConfig
        self._Modules: dict[str, ...] = modules if modules is not None else dict()
        return

    def get_core_config(self) -> dict[str, ...]:
        """Get the core configuration. Can only get once!"""
        if Config._core_lock:
            raise RuntimeError("Core config is already retrieved!")
        # Lock core config
        Config._core_lock = True
        return copy.deepcopy(self._Core)

    def set_core_config(self, config: dict[str, ...]) -> None:
        """Set the core configuration."""
        # Release lock core config
        Config._core_lock = False
        self._Core = copy.deepcopy(config)
        return

    def apply_core_patch(self, config: dict[str, ...]) -> None:
        """Apply a new patch to core configuration."""
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

    def get_module_config(self, module_name: str) -> dict[str, ...]:
        """Get the module configuration. Can only get once!"""
        lock_name = f"{module_name}_lock"
        assert not getattr(self, lock_name, False), f"{module_name} config is already retrieved!"
        # Lock module config
        setattr(self, lock_name, True)
        if module_name not in self._Modules.keys():
            # Make placeholder
            self._Modules[module_name] = dict()
        return copy.deepcopy(self._Modules[module_name])

    def set_module_config(self, module_name: str, config: dict[str, ...]) -> None:
        """Set the module configuration."""
        # Release lock module config
        lock_name = f"{module_name}_lock"
        setattr(self, lock_name, False)
        self._Modules[module_name] = copy.deepcopy(config)
        return

    def apply_module_config(self, module_name: str, config: dict[str, ...]) -> None:
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
    def json_decode_hook(json_obj) -> Config:
        """(Internal) Object hook for JSONDecoder."""
        if "Core" in json_obj and "Modules" in json_obj:
            return Config(core=json_obj["Core"], modules=json_obj["Modules"])


global_config: Config


def make_config_global(cfg: Config):
    """(Internal) Makes the config class global."""
    global global_config
    global_config = cfg


def pass_config(f: Callable) -> Callable:
    """Automatically passes the global config as first parameters to all decorated function."""

    @wraps(f)
    def wrapper(*args, **kwargs) -> ...:
        return f(global_config, *args, **kwargs)

    return wrapper
