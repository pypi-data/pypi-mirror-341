import inspect
import os
import sys
from pathlib import Path
import pytest


from hpe_opsramp_cli.singleton_logger import SingletonLogger


try:
    # This code is to run as module
    from hpe_opsramp_cli.opsramp_environment import OpsRampEnvironment
except ModuleNotFoundError:
    # this code is to run as python file
    current_dir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    project_root = Path(current_dir).parent.parent
    sys.path.append(project_root)

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    )
    # rich.print(sys.path)
    print(sys.path)
    from src.hpe_opsramp_cli.opsramp_environment import OpsRampEnvironment


def test_get_environment() -> None:
    envname = "UAT_BalaSubramanian_API"
    envfile = "environments.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)
    env_dict = env.get_environment()
    # {'client_id': '', 'client_secret': '', 'name': 'UAT_BalaSubramanian_API', 'partner': '', 'tenant': '', 'url': ''}
    # rich.print(env_dict)
    assert "client_secret" in env_dict
    assert "client_id" in env_dict
    assert "name" in env_dict
    assert "tenant" in env_dict
    assert "url" in env_dict


def test_get_env_valid_yaml_valid_token() -> None:
    envname = "UAT_BalaSubramanian_API"
    envfile = "environments.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)
    token = env.get_token()
    assert token != ""


def test_get_env_valid_yaml_invalid_token() -> None:
    envname = "UAT_BalaSubramanian_API"
    envfile = "environments-wrong.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)

    """
    with pytest.raises(SSLError) as exe_info:
        env.get_token()
    rich.print(exe_info)"
    """

    with pytest.raises(SystemExit) as exc_info:
        env.get_token()
    assert exc_info.value.code == 1


def test_get_env_relative_path() -> None:
    envname = "UAT_BalaSubramanian_API"
    envfile = "environments.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)
    token = env.get_token()
    assert token != ""


def test_get_env_aboslute_path() -> None:
    from pathlib import Path

    envname = "UAT_BalaSubramanian_API"
    envfile = Path(
        "C:\\Users\\vetrivel\\src\\GitHub\\hpe-opsramp-cli\\environments.yml"
    )
    env = OpsRampEnvironment(envname=envname, envfile=envfile)
    token = env.get_token()
    assert token != ""


def test_do_post() -> None:
    envname = "netenrich_test"
    envfile = "environments.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)

    opsql_query = env.get_json_from_file("opsql.json")
    post_response = env.do_post(opsql_query, api_name="opsql")
    # rich.print(post_response)
    assert "clientId" in post_response[0]


def test_do_post1() -> None:
    logger = SingletonLogger().get_logger("DEBUG")
    envname = "UAT_National_INC"
    envfile = "environments.yml"
    env = OpsRampEnvironment(envname=envname, envfile=envfile)

    opsql_query = env.get_json_from_file("opsql.json")
    post_response = env.do_post(opsql_query, api_name="opsql")
    # rich.print(post_response)
    assert "clientId" in post_response[0]
