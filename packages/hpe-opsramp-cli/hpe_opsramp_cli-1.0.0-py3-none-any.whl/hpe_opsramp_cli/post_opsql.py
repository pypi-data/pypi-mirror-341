import json
from typing import Optional

import rich
import typer
from typing_extensions import Annotated

from hpe_opsramp_cli import cli_utils as CLI_Utils
from hpe_opsramp_cli import opsramp_environment as OpsRampEnvironment

app = typer.Typer()

opsramp_cli_app = typer.Typer()
app.add_typer(opsramp_cli_app, name="hpe_opsramp_cli")

# command help messages
env_help = "Name of environment to use, as defined in your environments.yml file"
envfile_help = "Location of environments YAML file"
envfile_default = "environments.yml"
opsql_file_help = "Location of the OpsQL input payload JSON file"
opsql_file_default = "opsql.json"


# @app.command()
@opsramp_cli_app.command("post_opsql")
def post_opsql(
    env: Annotated[str, typer.Option(help=env_help)],
    envfile: Annotated[
        Optional[str], typer.Option(help=envfile_help)
    ] = envfile_default,
    opsql_file: Annotated[
        Optional[str], typer.Option(help=opsql_file_help)
    ] = opsql_file_default,
):
    rich.print("post_opsql:")
    rich.print_json(json.dumps(locals()))
    opsramp_environment = OpsRampEnvironment(envname=env, envfile=envfile)
    CLI_Utils.do_cmd_post_opsql(opsramp_environment, locals())


"""
To Test
python post_opsql.py hpe_opsramp_cli post_opsql --help
python post_opsql.py hpe_opsramp_cli post_opsql --env UAT_BalaSubramanian_API
I

"""
if __name__ == "__main__":
    app()
