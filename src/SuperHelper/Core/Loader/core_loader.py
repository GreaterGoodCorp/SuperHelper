# This module defines the module loader function.

# Import CLI config loader function
from SuperHelper.Core.Helper.Config import load_cli_config

# Load CLI config
cli_config = load_cli_config(verbose=True, ignore_error=False)

# Module loader function
def load_installed_module(*, verbose=False, ignore_error=False):
    pass
