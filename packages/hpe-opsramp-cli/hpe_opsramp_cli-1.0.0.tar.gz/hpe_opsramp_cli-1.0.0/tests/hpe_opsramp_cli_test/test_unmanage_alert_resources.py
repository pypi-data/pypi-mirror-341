from typing import List

from typer.testing import CliRunner

import rich

try:
    from src.hpe_opsramp_cli.unmanage_alert_resources import app
except ModuleNotFoundError:
    from hpe_opsramp_cli.unmanage_alert_resources import app

runner = CliRunner()


def test_unmanage_alert_resources_default_environment() -> None:
    """

    :return:

    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
    ]
    result = runner.invoke(app, test_args)

    # assert result.exit_code == 0  # Use result.stdout to access the command's output
    """
    To DO
    <Result SSLError(MaxRetryError("HTTPSConnectionPool(host='uat.opsramp.net', port=443): Max retries exceeded with url: /opsql/api/v3/tenants/cc0c2a2e-9c63-46b5-9db2-ec9f6d7dbcbd/queries (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:997)')))"))>
    """

    # output = result.stdout.rstrip()


def test_unmanage_alert_resources_log_level() -> None:
    """

    :return:

    """
    test_args: List[str] = [
        "--log_level",
        "DEBUG",
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
    ]
    result = runner.invoke(app, test_args)

    assert result.exit_code == 0  # Use result.stdout to access the command's output
    output = result.stdout.rstrip()
    rich.print(output)


def test_unmanage_alert_resources_invalid_log_level() -> None:
    """

    :return:

    """
    test_args: List[str] = [
        "--log_level1",
        "DEBUG1",
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
    ]
    result = runner.invoke(app, test_args)

    assert result.exit_code == 2  # Use result.stdout to access the command's output
    output = result.stdout.rstrip()

    rich.print(output)


def test_unmanage_alert_resources_invalid_env() -> None:
    """

    Negative Test case to test with invalid env

    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API1",
    ]
    result = runner.invoke(app, test_args)

    assert result.exit_code != 0
    output = result.stdout.rstrip()
    # assert "is not found in the environment file" in output


def test_unmanage_alert_resources_help() -> None:
    """

    Negative Test case to test with invalid env
    uv run -m pytest -k "test_unmanage_alert_resources_help"

    """
    test_args: List[str] = ["unmanage_alert_resources", "--help"]
    result = runner.invoke(app, test_args)

    assert result.exit_code == 0
    output = result.stdout.rstrip()
    print(output)
    # assert "is not found in the environment file" in output


def test_unmanage_alert_resources_relative_path1() -> None:
    """
    Positive Test case to test with relative_path
    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
        "--env-file",
        "..\\..\\..\\..\\namasivaya\\opsrampcli\\environments.yml",
    ]
    result = runner.invoke(app, test_args)

    # assert result.exit_code == 0
    # output = result.stdout.rstrip()
    # assert "is not found in the environment file" in output


def test_unmanage_alert_resources_absolute_path() -> None:
    """
    Positive Test case to test with absolute path

    uv run -m pytest -k "test_unmanage_alert_resources_absolute_path"
    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
        "--env-file",
        "C:\\Users\\vetrivel\\namasivaya\\opsrampcli\\environments.yml",
    ]
    result = runner.invoke(app, test_args)

    assert result.exit_code == 0


def test_unmanage_alert_resources_relative_path2() -> None:
    """
    Positive Test case to test
    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
        "--env-file",
        "environments.yml",
    ]
    result = runner.invoke(app, test_args)

    # assert result.exit_code == 0


def test_unmanage_alert_resources_wrong_token() -> None:
    """
    Positive Test case to test with relative_path
    """
    test_args: List[str] = [
        "unmanage_alert_resources",
        "--env",
        "UAT_BalaSubramanian_API",
        "--env-file",
        "C:\\Users\\vetrivel\\namasivaya\\opsrampcli\\environments-wrong.yml",
    ]
    result = runner.invoke(app, test_args)

    assert result.exit_code != 0
