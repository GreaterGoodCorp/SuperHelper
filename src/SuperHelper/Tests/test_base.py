import click.testing
import pytest

from SuperHelper.Core import cli, run_startup, save_config

runner: click.testing.CliRunner = click.testing.CliRunner()


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    global runner
    run_startup()
    runner = click.testing.CliRunner()
    yield
    save_config()


def run(args: str = None) -> click.testing.Result:
    return runner.invoke(cli, args)


__all__ = [
    "setup_and_cleanup",
    "run",
]
