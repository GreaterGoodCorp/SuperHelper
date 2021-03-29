# Subpackage `SuperHelper.Core.Utils`

This package contains utilities implemented exclusively for the `core_cli.py` module. APIs designed in this subpackage
are intended for internal use Sonly.

Core commands are also documented here.

## Package content

1. Module `command.py`: Contains the core commands.

2. Module `loader.py`: Contains the module loader function.

## API documentation

1. Function `load_installed_modules()`

  * **Parameters**: *No parameter*
      
  * **Returns**: A list of main methods of each installed module.

  * **Raises**: 
    
    * `ImportError` if the module cannot be imported.
    
    * `AttributeError` if the module does not contain a `main()` function decorated as either `@click.command` or
      `@click.group`
  
  * **Note**: This function is intended for internal use only. It should only be called once when the application loads
    modules. (Called by Core CLI)
    
2. Function `load_core_modules()`

  * **Parameters**: *No parameter*
      
  * **Returns**: A list of core command utilities.

  * **Note**: This function is intended for internal use only. It should only be called once when the application loads
    modules. (Called by Core CLI)
  
## Command documentation

1. Command `install`

  * **Usage**: `helper install <MODULES>` where `<MODULES>` are names of modules you wish to install.
  
  * **Notes**: This command is used to install any builtin or external modules that are not installed yet.
  
2. Command `uninstall`

  * **Usage**: `helper uninstall <MODULES>` where `<MODULES>` are names of modules you wish to uninstall.
  
  * **Notes**: This command is used to uninstall any builtin or external modules that are installed.

3. Command `list`

  * **Usage**: `helper list [-a]`, when `-a` (or `--all`) is enabled, this will also list not installed modules.
  
  * **Notes**: This command is used to list available modules (installed or not installed)
