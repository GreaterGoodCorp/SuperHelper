# Subpackage `SuperHelper.Core.Config`

This package contains the configuration parser and the configuration manager

## Package content

1. Module `config_class.py`: Contains the definition of the configuration manager, the `Config` class.

2. Module `app_config.py`: Contains the I/O parser for `Config` class.

## API documentation

### `Config` class

The configuration manager for this entire application is defined in `Config` class. It makes using config easier
and more intuitive.

Design considerations:

* *`Singleton`-based*: Only one instance of `Config` class is available to access. It will automatically instantiated
  when the application starts.
  
* *`Lock`-based*: Caller can request the configuration be locked if it needs to modify the config. Others cannot request
  copies of the locked configuration.
  
* *`Deepcopy`-based*: All configuration dictionaries passing through or returned by the class is a deep-copied dictionary.

### Method documentation

1. Method `get_core_config(self) -> dict[str, ...]`

    This method returns the configuration of core CLI. Please note that it will be locked the entire time to prevent
    unauthorised access. `RuntimeError` is raised for any attempt to call this method.
  
    * *Parameters*: *No parameter required*

2. Method `set_core_config(self, config: dict[str, ...]) -> None`

    This method receives the configuration of core CLI and writes it to `Config` class. This method should only be called
    by the core CLI, as any modification to the core CLI will be overwritten when the application finalises.
  
    * *Parameters*: *`config` - The configuration of core CLI*

3. Method `apply_core_patch(self, config: dict[str, ...]) -> None`

    Unlike `Config.set_core_config`, this method does not overwrite the entire core configuration. Instead, it will apply
    any new keys in the `config` provided to the existing configuration. This method is used when a new key is introduced
    to the configuration, and to maintain backward compatibility with previous config.
  
    * *Parameters*: *`config` - The patch of core configuration*

4. Method `get_module_config(self, module_name: str) -> dict[str, ...]`

    This method returns the configuration of the module `module_name`. Please note that it will be locked the entire
    time to prevent unauthorised access. `RuntimeError` is raised for any attempt to call this method before
    `Config.set_module_config` is called with the same `module_name` provided.
  
    * *Parameters*: *`module_name` - The name of the module*

2. Method `set_module_config(self, module_name: str, config: dict[str, ...]) -> None`

  This method receives the configuration of the module `module_name` and writes it to `Config` class. This method should 
  be called by the caller of `Config.get_module_config` before returning.
  
  * *Parameters*: * *`config` - The configuration of core CLI*

                  * *``*

3. Method `apply_core_patch(self, config: dict[str, ...]) -> None`

  Unlike `Config.set_core_config`, this method does not overwrite the entire core configuration. Instead, it will apply
  any new keys in the `config` provided to the existing configuration. This method is used when a new key is introduced
  to the configuration, and to maintain backward compatibility with previous config.
  
  * *Parameters*: *`config` - The patch of core configuration*

5. Function `load_app_config()`

* **Parameters**:

  * `config_path`: The path to config file

    The path will be retrieved from the environment variable `SUPER_HELPER_CONFIG_PATH` if it is set. Otherwise, the
    default path is
    `Pathlib.Path.home() / ".super_helper"`

* **Returns**: *None*

* **Raises**:

  * `OSError` if either the path provided by environment variable `SUPER_HELPER_CONFIG_PATH` is a folder, or the config
    file does not exist at all, or is unreadable.

  * `JSONDecodeError` if the JSON document is invalid, or likely corrupted.

* **Note**: This function is intended for internal use only. It should only be called once when the application
  starts. (Called by Core CLI)


2. Function `save_app_config()`

* **Parameters**:

  * `config_path`: The path to config file

    The path will be retrieved from the environment variable `SUPER_HELPER_CONFIG_PATH` if it is set. Otherwise, the
    default path is
    `Pathlib.Path.home() / ".super_helper"`

* **Returns**: *None*

* **Raises**:

  * `OSError` if either the path provided by environment variable `SUPER_HELPER_CONFIG_PATH` is a folder, or the
    existing config file there is un-writable.

  * This function will not raise `JSONEncodeError` if there are non JSON-serializable values. Instead, it will be
    default to `None`.

* **Note**: This function is intended for internal use only. It should only be called once when the application ends. (
  Called by Core CLI)


3. Function `load_cli_config()`

* **Parameters**: *No parameter*

* **Returns**: The `CORE_CLI` section of the application configuration.

* **Note**: This function is intended for internal use only. It should only be called once when the application starts
  loading modules.
  (Called by the Core module loader)


4. Function `save_cli_config()`

* **Parameters**:

  * `config`: The configuration of CLI core

    This configuration is likely the CLI configuration returned by `load_cli_config()` after modifying its items.

* **Returns**: *None*

* **Note**: This function is intended for internal use only. It should only be called once when the application starts
  loading modules.
  (Called by the Core module loader)


5. Function `load_module_config()`

* **Parameters**:

  * `module_name`: The name of the module.

    It is highly recommended that the module will use its qualified name of the ***subpackage*** to maintain
    consistency.

* **Returns**: The configuration section of the module.

  If the module is run for the first time, this function will return an empty dict `dict()`. It might be saved into the
  application config when passed to `save_module_config()` with the same `module_name` provided.

* **Note**: All modules are not allowed to implement its own configuration handler. Modules must retrieve the
  configuration for themselves using this function, and save it using `save_module_config()` with the same `module_name`
  .


6. Function `save_module_config()`

* **Parameters**:

  * `module_name`: The name of the module.

    It is highly recommended that the module will use its qualified name of the ***subpackage*** to maintain
    consistency.

  * `config`: The configuration of the module.

    This configuration must be a `dict` and contains JSON-serializable items only. Non JSON-serializable items are
    serialized as `None`, which may lead to data loss if not used properly.

* **Returns**: *None*

* **Note**: All modules are not allowed to implement its own configuration handler. Modules must save its configuration
  using this function.
