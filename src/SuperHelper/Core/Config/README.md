# Subpackage `SuperHelper.Core.Config`

This package contains configuration loaders and savers for the application, the CLI core and other modules.

## Package content

1. Module `app_config.py`: Contains the configuration loader and saver for the application.

2. Module `cli_config.py`: Contains the configuration loader and saver for the CLI core.

3. Module `module_config.py`: Contains the configuration loader and saver for all modules.

## API documentation

1. Function `load_app_config()`

  * **Parameters**:
    
    * `config_path`: The path to config file
    
      The path will be retrieved from the environment variable `SUPER_HELPER_CONFIG_PATH` if it is set. Otherwise, the default path is
      `Pathlib.Path.home() / ".super_helper"`
      
  * **Returns**: *None*

  * **Raises**: 
    
    * `OSError` if either the path provided by environment variable `SUPER_HELPER_CONFIG_PATH` is a folder, or the config file does
      not exist at all, or is unreadable.
      
    * `JSONDecodeError` if the JSON document is invalid, or likely corrupted.
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application starts. (Called by Core CLI)
  
  
2. Function `save_app_config()`

  * **Parameters**:
    
    * `config_path`: The path to config file
    
      The path will be retrieved from the environment variable `SUPER_HELPER_CONFIG_PATH` if it is set. Otherwise, the default path is
      `Pathlib.Path.home() / ".super_helper"`
      
  * **Returns**: *None*

  * **Raises**:

    * `OSError` if either the path provided by environment variable `SUPER_HELPER_CONFIG_PATH` is a folder, or the existing config file there is
      un-writable.
      
    * This function will not raise `JSONEncodeError` if there are non JSON-serializable values. Instead, it will be default to `None`.
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application ends. (Called by Core CLI)
  
  
3. Function `load_cli_config()`

  * **Parameters**: *No parameter*
      
  * **Returns**: The `CORE_CLI` section of the application configuration.
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application starts loading modules.
    (Called by the Core module loader)
   

4. Function `save_cli_config()`

  * **Parameters**:

    * `config`: The configuration of CLI core

      This configuration is likely the CLI configuration returned by `load_cli_config()` after modifying its items.
      
  * **Returns**: *None*
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application starts loading modules.
    (Called by the Core module loader)
   

5. Function `load_module_config()`

  * **Parameters**:

    * `module_name`: The name of the module.

      It is highly recommended that the module will use its qualified name of the ***subpackage*** to maintain consistency.
      
  * **Returns**: The configuration section of the module.

    If the module is run for the first time, this function will return an empty dict `dict()`. It might be saved into the application config when
    passed to `save_module_config()` with the same `module_name` provided.
  
  * **Note**: All modules are not allowed to implement its own configuration handler. Modules must retrieve the configuration for themselves using
    this function, and save it using `save_module_config()` with the same `module_name`.
    
 
6. Function `save_module_config()`

  * **Parameters**:

    * `module_name`: The name of the module.

      It is highly recommended that the module will use its qualified name of the ***subpackage*** to maintain consistency.
      
    * `config`: The configuration of the module.

      This configuration must be a `dict` and contains JSON-serializable items only. Non JSON-serializable items are serialized as `None`, which may
      lead to data loss if not used properly.
      
  * **Returns**: *None*
  
  * **Note**: All modules are not allowed to implement its own configuration handler. Modules must save its configuration using this function.
