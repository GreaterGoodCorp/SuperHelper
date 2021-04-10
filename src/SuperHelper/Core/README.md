# Subpackage `SuperHelper.Core`

This subpackage contains the implementation of core CLI, including a configuration manager for all modules.

## Package content

1. Subpackage `SuperHelper.Core.Config`: Contains the configuration parser and the configuration manager.

2. Subpackage `SuperHelper.Core.Utils`: Contains utilities implemented exclusively for the core CLI.

3. Module `core_cli.py`: Contains the structure of core CLI and the program entry point.

## API documentation

### Subpackage documentation

Documentation for subpackages are available in the `README.md` file in their respective locations.

### Standalone functions

1. Function `validate_no_win32() -> None`

   This function is intended for internal use only. It asserts that the system platform is strictly not `win32`, as the
   OS is not supported by this program.

   This function raises `AssertionError` if the system is indeed `win32`.

   *Parameters*: *No parameter required*

2. Function `main_entry() -> NoReturn`

   This function is intended for internal use only. It serves as the main entry point of the program, which is called by
   a script created by `setup.py` is run.

   *Parameters*: *No parameter required*

### Other functions

1. Function `cli() -> int`

   This function is intended for internal use only. It serves as the group command of other subcommands (either core
   commands or modules' `main()` function).

   *Parameters*: *No parameter required*
