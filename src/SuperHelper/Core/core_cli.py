# This module defines the entry Click CLI function
# All modules of SuperHelper should define its own group, which can imported by this module.

# Import a loader function, which loads all the modules installed by user.
from SuperHelper.Core.Loader import load_installed_modules

# Import CLI builder
import click

# Program entry point
@click.group()
def cli():
    pass

# Load installed modules
installed_modules = load_installed_modules(verbose=True, ignore_import_error=True)

# Add installed modules to CLI entry point
for module in installed_modules:
    cli.add_command(module)
