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
      
  * **Returns**: `0` if the config is either loaded, or initialised successfully. Otherwise, returns `1`.
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application starts. (Called by Core CLI)
  
  
2. Function `save_app_config()`

  * **Parameters**:
    
    * `config_path`: The path to config file
    
      The path will be retrieved from the environment variable `SUPER_HELPER_CONFIG_PATH` if it is set. Otherwise, the default path is
      `Pathlib.Path.home() / ".super_helper"`
      
  * **Returns**: `0` if the config is either saved successfully. Otherwise, returns `1`.
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application ends. (Called by Core CLI)
  
