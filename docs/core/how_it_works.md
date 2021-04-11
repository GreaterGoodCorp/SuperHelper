# How does SuperHelper work internally?

At the first glance, `SuperHelper` seems to be very difficult to understand for some. On this page, I will be
demonstrating the internal workflow of the program.

## Table of content

* [Entry point](#entry-point)

* [Execution flows](#execution-flows)

* [A unified SuperHelper?](#why-must-we-put-all-these-modules-under-a-single-superhelper)

* [Module design](#module-design)

## Entry point

When the package is installed properly by `pip`, the package manager will create a Python script, which points to
the entry point of the package and is added to `PATH`. This allows the application to be called anywhere in a terminal.

The entry point for this package is the function `main_entry()` (located in `SuperHelper/Core/core_cli.py`)

## Execution flows

1. When a command is entered on the terminal, all options and arguments are passed as `sys.argv`. Then, control goes to
   the `main_entry()` function.
   
2. The function `main_entry()` will run the following setup:

   * First, it asserts that the platform `sys.platform` is not Windows (`win32`). This is because the application is not
     configured to work on a Windows machine. If the platform is indeed Windows, it catches the `AssertionError` raised
     by the internal `assert`, and exits with a non-zero code.
     
   * Secondly, it loads and configures the parent `logging.Logger` instance, setting up logging to both log files and to
     `sys.stderr`.
     
   * Next, it loads application config from path `SUPER_HELPER_CONFIG_PATH`. If not defined, it loads from default path.
   
   * After that, it imports all core commands and any added modules, respectively, and attaches them to the core CLI
     (`cli()`)

   * Finally, control goes to `cli()` to execute all commands.
   
3. The function `cli()` does not serve any special purpose, other than redirecting options and arguments to the
   respective core command or module.
   
4. The intended recipient then fulfills its task, outputs anything it requires, and either exits or returns control back
   to `main_entry()` function. Either way, `main_entry()` will always catch the `SystemExit` exception to perform
   post-ops functions. After that, it re-raises the `SystemExit` with the intended exit code, and exits the application.

## Why must we put all these modules under a single SuperHelper?

It is true that each module created for `SuperHelper` can exist as a standalone module. However, there are a lot of
drawbacks for this. For example, the module has to take care of its own configuration, cryptographic functions, and
logging, which results in loads of boilerplate code. The use of `SuperHelper` simplifies these things by providing a
simple interface for all of these tedious tasks. Full benefits under `SuperHelper` include, but not limited to:

* A unified configuration manager
  
* A ready-to-use set of utilities: Cryptography, Bitwise Ops, Logging

## Module design

It is hard to make sure that everyone sticks to a standard in designing modules for `SuperHelper`. However, there are
things that should be strictly followed.

Firstly, this application is built on `click` library. For more information, please visit
[its website](https://palletsprojects.com/p/click/). Hence, modules must implement its interface with `click.command` or
`click.group` in order to be integrated into `SuperHelper`. In addition, the module (in the form of a Python subpackage)
must provide an entry point `main()` decorated with either `click.command` or `click.group`.

Secondly, module should use the built-in configuration manager provided by `SuperHelper.Core.Config`. This allows future
patches to the config, or changes in location of the config file.

Thirdly, the use of other core utilities are not compulsory, but highly recommended so. This makes the user experience
more uniform across all modules.

And lastly, for modules that utilizes unit testing, the tests should be put in `SuperHelper.Tests` as a module prefixed
with `test_<MODULE_NAME>.py`. This allows Pytest to discover the tests automatically without any configuration.
