import click

from SuperHelper.Core.Essentials import *
from SuperHelper.Modules.Grapher import EquationParser, ExpressionParser
from SuperHelper.Modules.Grapher.parser import BinaryOps, Equation

ModuleName = "Grapher"
__name__, logger, ModuleDir = initialise_module(ModuleName)
CacheDir = ModuleDir / "Cache"


@pass_config(module_name=ModuleName)
def validate_equation(value, *_, **__):
    config = __["config"]
    is_generated = config.get("is_generated", False)
    eqn_cache_dir = CacheDir / "EquationParser"
    if not eqn_cache_dir.exists():
        eqn_cache_dir.mkdir(parents=True)
    if is_generated:
        parser = EquationParser(outputdir=str(eqn_cache_dir), debug=DEBUG, errorlog=logger, optimize=True)
    else:
        parser = EquationParser(outputdir=str(eqn_cache_dir), debug=DEBUG, errorlog=logger)
    parser.make_ast(value)
    if type(parser.ast) == Equation:
        return parser.generate_equation()
    else:
        try:
            expr = validate_expression(value)
            logger.warning("An expression is provided instead of an equation, assuming the expression is set to 0.")
            return (Equation(expr, 0)).pythonize()
        except click.UsageError:
            raise click.UsageError("Input must be an equation!")


@pass_config(module_name=ModuleName)
def validate_expression(value, *_, **__):
    config = __["config"]
    is_generated = config.get("is_generated", False)
    exp_cache_dir = CacheDir / "ExpressionParser"
    if not exp_cache_dir.exists():
        exp_cache_dir.mkdir(parents=True)
    if is_generated:
        parser = ExpressionParser(outputdir=str(exp_cache_dir), debug=DEBUG, errorlog=logger, optimize=True)
    else:
        parser = ExpressionParser(outputdir=str(exp_cache_dir), debug=DEBUG, errorlog=logger)
    parser.make_ast(value)
    if type(parser.ast) != BinaryOps:
        raise click.UsageError("Input must be an expression!")
    return parser.generate_function()


@click.group("math")
def main():
    """Solves maths on commandline."""
    pass


@main.command("solve")
@click.argument("equation", type=validate_equation, required=True)
def solve(equation):
    pass
