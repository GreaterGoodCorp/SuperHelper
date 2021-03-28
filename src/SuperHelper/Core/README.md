# Subpackage `SuperHelper.Core`

This subpackage contains the core functionalities of this program.

## Package content

- Subpackage `SuperHelper.Core.Helper`: Contains core helper methods to streamline the development process.


- Module `core_utils.py`: Contains top-level commands for CLI core, i.e. commands that do not belong to any module.


- Module `core_loader.py`: Contains a module loader functions, which loads installed modules.


- Module `core_cli.py`: Contains the main entry point of the program.

## Documentation

### CLI utilities

1. Command `install`

    * **Usage**: `helper install <MODULES>`, where `<MODULES>` are names of modules to install.
    
    * **Details**: This command checks if the module exists and is not installed yet, after that, the name of the module
      will be added to configuration file.
      

2. Command `uninstall`

    * **Usage**: `helper uninstall <MODULES>`, where `<MODULES>` are names of modules to uninstall.
    
    * **Details**: This command checks if the module is installed, after that, the name of the module will be added
      removed from configuration file.


3. Command `list`

    * **Usage**: `helper list [-a]`, where `-a` specifies whether to list not installed modules as well.
    
    * **Details**: This command scans through all available modules in `SuperHelper.Builtins` and
      `SuperHelper.External`, after that, it outputs all the names of the (installed) modules, or all modules (if `-a`)
      is specified.
      
### API

1. Function `load_core_utils()` (in `core_utils.py`)

    * **Parameters**: *Not applicable*
    
    * **Returns**: A list of `MethodType`, which are all the CLI utility functions defined in `core_utils.py`
    
    * **Notes**: This function is only used internally.


2. Function `load_installed_modules()` (in `core_loader.py`)

    * **Parameters**: *Not applicable*
    
    * **Returns**: A list of `MethodType`, which are the entry points of all installed modules, as reflected in the
      configuration file.
    
    * **Notes**: This function is only used internally.


3. Function `cli()` (in `core_cli.py`)

    * **Parameters**: *Not applicable*
    
    * **Returns**: *Not applicable*
    
    * **Notes**: This function is the CLI root of the program, which is intended to be used internally.
    

4. Function `main_entry()` (in `core_cli.py`)

    * **Parameters**: *Not applicable*
    
    * **Returns**: This function raises `SystemExit`.
    
    * **Notes**: This function is the entry point of the program, which is intended to be used internally.
