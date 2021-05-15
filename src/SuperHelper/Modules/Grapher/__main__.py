import click

from SuperHelper.Core.Essentials import *
from SuperHelper.Modules.Grapher import EquationParser, ExpressionParser

ModuleName = "Grapher"
__name__, logger, ModuleDir = initialise_module(ModuleName)
CacheDir = ModuleDir / "Cache"


def validate_equation(value, *_, **__):
    eqn_cache_dir = CacheDir / "EquationParser"
    eqn_cache_dir.mkdir(parents=True, exist_ok=True)
    parser = EquationParser(outputdir=eqn_cache_dir)
    parser.make_ast(value)
    return parser.ast


def validate_expression(value, *_, **__):
    exp_cache_dir = CacheDir / "ExpressionParser"
    exp_cache_dir.mkdir(parents=True, exist_ok=True)
    parser = ExpressionParser(outputdir=exp_cache_dir)
    parser.make_ast(value)
    return parser.generate_function()


@click.group("math")
def main():
    """Solves maths on commandline."""
    pass


@main.command("solve")
@click.argument("equation", type=validate_equation, required=True)
def solve(equation):
    pass
