import logging

from SuperHelper.Core.Config import load_module_config

import click

logger = logging.getLogger("SuperHelper.Builtins.UnitConverter")


@click.command("convert")
def main():
    config = load_module_config("SuperHelper.Builtins.UnitConverter")
    pass
