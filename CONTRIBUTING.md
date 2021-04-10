# Contributing to SuperHelper

Firstly, let me take this opportunity to thank you for deciding to contribute to this wonderful project, whether it is:

- Reporting a bug

- Discussing the current state of the code

- Submitting a fix

- Proposing new features

- Becoming a maintainer

## Platform

I use GitHub to host this open-source project, so any contributions should and will be made there!

## Workflow

Unless you are a maintainer, please follow the [GitHub Flow] to make sure that all changes to
the codebase go smoothly.

Here is a quick overview:

1. Fork the repo and create your branch from `main`.

2. If you've added code that should be tested, add tests.

3. If you've changed APIs, update the documentation.

4. Make sure your code lints.

5. Issue that pull request!

## Technical details

### Coding style

PEP8 should be the standard coding style for this project. However, it is not required to follow this standard to the
teeth; some exception can be made, such as:

* Line length: The limit is now 120 characters.

* Naming: Mostly PEP8 for internal functionalities, i.e. used only in a single module.

### Program flow

All core functionalities are defined in `SuperHelper.Core`. When the user executes a command, this happens:

1. Control goes to the `main_entry()` function, defined in `SuperHelper.Core.core_cli`.

    - Application configuration is loaded. (`load_app_config()` in `SuperHelper.Core.Helper.Config`)

    - Core utilities, i.e. tools that are not attached to any modules, are loaded. (`load_cli_utils()`
      in `SuperHelper.Core.core_utils`)

    - All installed modules are loaded. (`load_installed_modules()` in `SuperHelper.Core.Loader`)

2. Control goes to whatever module the user has indicated.

    - Module loads its own configuration. (`load_module_config()` in `SuperHelper.Core.Helper.Config`)

    - Module fulfills its functionalities.

    - Module finishes up its post-functionalities cleanup, i.e. saving its own configuration, etc.

    - Module calls `sys.exit()` to return control to Core CLI.

3. Control goes back to Core CLI (`main_entry()`)

    - Core saves the entire application configuration.
    
    - Core re-raises `SystemExit` to end the program.


### Adding new modules to SuperHelper

External modules are now moved to a different repositories! Please follow the contribution guidelines as stated there.

### Improving / Fixing existing modules in SuperHelper

Since most modules will be created by people other than myself, please open an [issue][Issues]
first to consult the creator. In the event of urgent bugs (including security vulnerabilities),
please [email me.](mailto:binhnt.mdev@gmail.com)

### Improving / Fixing Core CLI

Core CLI is the cornerstone of this entire program, hence all fixes and improvements are welcomed, either by opening an
[issue][Issues], or sending a pull request!

Please note that the Core API can be added but not removed (for backward compatibility)!

## Any contributions you make will be under the MIT Software Licence
In short, when you submit code changes, your submissions are understood to be under the same [MIT License].
Feel free to contact the maintainers if that's a concern.

## License
By contributing, you agree that your contributions will be licensed under its [MIT License].

[Github Flow]: https://guides.github.com/introduction/flow/index.html
[MIT License]: https://github.com/GreaterGoodCorp/SuperHelper/blob/main/LICENSE
[Issues]: https://github.com/GreaterGoodCorp/SuperHelper/issues
[EMAIL]: mailto:binhnt.mdev@gmail.com
