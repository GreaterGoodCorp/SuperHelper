# Subpackage `SuperHelper.Core.Utils`

This subpackage contains utilities implemented exclusively for the core CLI. APIs designed in this subpackage are
intended for internal use only.

Core commands are also documented here.

## Package content

1. Module `command.py`: Contains the core commands.

2. Module `loader.py`: Contains the module loader function.

3. Module `logger.py`: Contains the core logger initialisation function.

## API documentation

### Class `TracebackInfoFilter(logging.Filter)`

This class inherits from `logging.Filter`. This filter allows traceback to get logged into the log file, while blocking
it from `sys.stderr`.

### Standalone functions

1. Function `load_installed_modules(config: dict[str, ...]) -> list[tuple[click.Command, str]]`

   This function is intended for internal use only. It takes in the core config (passed in by the decorator), and
   returns a list of `click.Command` objects of added modules.

   *Parameters*: *No parameter required*

2. Function `load_core_commands() -> list[tuple[click.Command, str]]`

   This function is intended for internal use only. It is a helper function, which returns all core commands defined in
   the module.

   *Parameters*: *No parameter required*

3. Function `initialise_core_logger(logging_path: str) -> logging.Logger`

   This function is intended for internal use only. It is called by the core CLI when the application starts to
   initialize the logger.

   *Parameters*: *`logging_path` - Path to log file*

### Command documentation

1. Command `add`

* **Usage**: `helper add <MODULES>` where `<MODULES>` are names of modules you wish to add.

* **Notes**: This command is used to add any modules that are not added yet.

2. Command `remove`

* **Usage**: `helper remove <MODULES>` where `<MODULES>` are names of modules you wish to remove.

* **Notes**: This command is used to remove any modules that are added.

3. Command `list`

* **Usage**: `helper list`

* **Notes**: This command is used to list all installed modules (added or not added)
