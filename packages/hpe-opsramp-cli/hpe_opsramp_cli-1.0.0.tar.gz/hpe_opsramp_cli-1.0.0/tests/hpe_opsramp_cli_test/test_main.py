from typing import List


from typer.testing import CliRunner

import rich

try:
    from src.hpe_opsramp_cli.main import app
except ModuleNotFoundError:
    from hpe_opsramp_cli.main import app

runner = CliRunner()


def test_help() -> None:
    """
    :return:
    """
    test_args: List[str] = [
        "--help",
    ]
    result = runner.invoke(app, test_args)

    rich.print(result.stdout)

    assert result.exit_code == 0  # Use result.stdout to access the command's output


def test_log_level() -> None:
    """
    :return:

    to run from command line 
    opsramp-cli --log-level DEBUG --help
    """
    test_args: List[str] = ["opsramp-cli", "--log-level", "DEBUG", "--help"]
    result = runner.invoke(app, test_args)

    rich.print(result.stdout)

    assert result.exit_code == 0  # getting error No such command 'opsramp-cli'
