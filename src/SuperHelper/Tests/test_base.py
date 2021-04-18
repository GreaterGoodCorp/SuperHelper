import pathlib

import click.testing
import pytest

from SuperHelper.Core import cli, run_startup, save_config

runner: click.testing.CliRunner = click.testing.CliRunner()
__all__ = [
    "setup_and_cleanup",
    "test_data_dir",
    "run",
]


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    global runner
    run_startup()
    runner = click.testing.CliRunner()
    yield
    save_config()


@pytest.fixture()
def test_data_dir():
    return pathlib.Path(__file__).parent.absolute() / "data"


def run(args: str = None) -> click.testing.Result:
    return runner.invoke(cli, args)
