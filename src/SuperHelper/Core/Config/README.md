# Subpackage `SuperHelper.Core.Config`

This package contains the configuration parser and the configuration manager

## Package content

1. Module `config_class.py`: Contains the definition of the configuration manager, the `Config` class.

2. Module `app_config.py`: Contains the I/O parser for `Config` class.

## API documentation

### `Config` class

The configuration manager for this entire application is defined in `Config` class. It makes using config easier and
more intuitive.

Design considerations:

* *`Singleton`-based*: Only one instance of `Config` class is available to access. It will automatically be instantiated
  when the application starts.

* *`Lock`-based*: Caller can request the configuration be locked if it needs to modify the config. Others cannot request
  copies of the locked configuration.

* *`Deepcopy`-based*: All configuration dictionaries passing through or returned by the class is a deep-copied
  dictionary.

#### Method documentation

1. Method `get_core_config(self) -> dict[str, ...]`

   This method returns the configuration of core CLI. Please note that it will be locked the entire time to prevent
   unauthorized access. `RuntimeError` is raised for any attempt to call this method.

   *Parameters*: *No parameter required*

2. Method `set_core_config(self, config: dict[str, ...]) -> None`

   This method receives the configuration of core CLI and writes it to `Config` class. This method should only be called
   by the core CLI, as it will overwrite any modified configurations.

   *Parameters*:

   * *`config` - The configuration of core CLI*

   * *`lock` - Whether to set the lock for the module config*

3. Method `apply_core_patch(self, config: dict[str, ...]) -> None`

   Unlike `Config.set_core_config`, this method does not overwrite the entire core configuration. Instead, it will apply
   any new keys in the `config` provided to the existing configuration. This method is used when a new key is introduced
   to the configuration, and to maintain backward compatibility with previous configs.

   *Parameters*: *`config` - The patch of core configuration*

4. Method `get_module_config(self, module_name: str, lock: bool = True) -> dict[str, ...]`

   This method returns the configuration of the module `module_name`. If `lock` is left default or set to True, the
   module configuration will be locked the entire time to prevent unauthorized access. `RuntimeError` is raised for any
   attempt to call this method before `Config.set_module_config` is called with the same `module_name` provided.

   *Parameters*:

   * *`module_name` - The name of the module*

   * *`lock` - Whether to set the lock for the module config*

5. Method `set_module_config(self, module_name: str, config: dict[str, ...]) -> None`

   This method receives the configuration of the module `module_name` and writes it to `Config` class. This method
   should be called by the caller of `Config.get_module_config` before returning.

   *Parameters*:

   * *`module_name` - The name of the module*

   * *`config` - The configuration of core CLI*

6. Method `apply_module_patch(self, config: dict[str, ...]) -> None`

   Unlike `Config.set_module_config`, this method does not overwrite the entire module configuration. Instead, it will
   apply any new keys in the `config` provided to the existing configuration. This method is used when a new key is
   introduced to the configuration, and to maintain backward compatibility with previous configs.

   *Parameters*:

   * *`module_name` - The name of the module*

   * *`config` - The patch of module configuration*

#### Other methods

1. Overriding method `__dict__(self) -> dict[str, ...]`

   This overriding method returns a dictionary of the `Core` and `Modules` configuration (`dict[str, dict[str, ...]]`).
   It is usually only used for JSON serialization.

   *Parameters*: *No parameter required*

2. Static method `json_decode_hook(json_obj: ...) -> Config`

   This method is intended for internal use only. This method is used by JSON decoder to return the `Config` object.

   *Parameters*: *`json_obj` - The JSON object passed in by JSON decoder*

### Other API functions

1. Function `make_config_global(cfg: Config) -> None`

   This function takes in a `Config` instance and makes it global (in the scope of the module `config_class.py`). This
   allows for a more intuitive way to access the config.

   This function should only be called once by the core CLI.

   *Parameters*: *`cfg`: The `Config` instance*

2. Decorator `pass_config(core: bool = None, module_name: str = None) -> Callable`

   This decorator will pass the `Config` instance as the first positional parameter of the decorated function call.
   (if both `core` and `module_name` are left default).

   If `core is not None`, this decorator will pass the configuration of core CLI instead. If `module_name is not None`,
   this decorator will pass the configuration of module `module_name`.

   This default decorator should be used if the config will be modified. The quicker ways (by setting either `core` or
   `module_name`) can only be used if the config will not be modified, as the config returned is not locked.

   If both are not `None`, this decorator raises `ValueError`.

   *New*: A parameter (`lock`) is added to optionally lock the config. This change will make most `Config`'s instance
   method largely redundant for end-developers.

   *Parameters*:

   * *`core` - Whether to return only the configuration of core CLI*

   * *`module_name` - The name of the module to get configuration*

   * *`lock` - Whether to lock the config*

3. Function `is_debug() -> bool`

   This function returns the value of entry `Debug` in the core CLI (when it is first loaded). This allows any function
   to get the value without directly accessing the configuration of core CLI.

   *Parameters*: *No parameter required*\

4. Function `load_app_config(config_path: str) -> None`

   This function is intended for internal use only. It takes in the path of the config file, parses the information to a
   `Config` instance, and makes it global.

   This function should only be called once by the core CLI.

   *Parameters*: *`config_path`: Path to config file*

5. Function `save_app_config(config_path: str) -> None`

   This function is intended for internal use only. It takes in the path of the config file, dumps the global `Config`
   object into JSON text, and writes the text to the config file.

   This function should only be called once by the core CLI.

   *Parameters*: *`config_path`: Path to config file*
