import click

from SuperHelper.Core.Essentials import *

ModuleName = "Grapher"
__name__, logger, ModuleDir = initialise_module(ModuleName)


def validate_equation():
    # TODO: Do tokenization here!
    pass


@click.group("math")
def main():
    """Solves maths on commandline."""
    pass


@main.command("solve")
@click.argument("equation", type=validate_equation, required=True)
def solve(equation):
    pass
