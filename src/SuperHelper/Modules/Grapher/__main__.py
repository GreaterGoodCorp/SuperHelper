import click

from SuperHelper.Core.Essentials import *

ModuleName = "Grapher"
__name__, logger, ModuleDir = initialise_module(ModuleName)


@click.command()
def main():
    """Solves maths on commandline."""
    pass
