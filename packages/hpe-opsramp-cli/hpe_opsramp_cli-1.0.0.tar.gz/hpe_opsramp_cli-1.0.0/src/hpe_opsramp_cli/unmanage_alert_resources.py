from typing import Optional

import typer
from typing_extensions import Annotated

# from opentelemetry.instrumentation.auto_instrumentation import AutoInstrumentor
# from opentelemetry.instrumentation.auto_instrumentation

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry import trace

from hpe_opsramp_cli import settings as s
from hpe_opsramp_cli.cli_utils import CLI_Utils
from hpe_opsramp_cli.opsramp_environment import OpsRampEnvironment
from hpe_opsramp_cli.singleton_logger import SingletonLogger


"""
Error while running from test ModuleNotFoundError: No module named 'cli_utils'
Fixed while giving as src.hpe_opsramp_cli. ...
"""

app = typer.Typer(rich_markup_mode="markdown")

opsramp_cli_app = typer.Typer(rich_markup_mode="markdown")
app.add_typer(opsramp_cli_app)


# app.add_typer(opsramp_cli_app, name=s.PARENT_COMMAND)

# Auto-instrument Typer app
# AutoInstrumentor().instrument()

# Set up OpenTelemetry tracer provider
trace.set_tracer_provider(TracerProvider())

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Add span processor to tracer provider
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

logger = SingletonLogger().get_logger()


# @app.command()
@opsramp_cli_app.command(s.UNMANAGE_ALERT_RESOURCES_SUB_COMMAND)
def unmanage_alert_resources(
    env: Annotated[str, typer.Option(help=s.ENV_HELP)],
    env_file: Annotated[
        Optional[str], typer.Option(help=s.ENV_FILE_HELP)
    ] = s.ENV_FILE_DEFAULT,
    opsql_file: Annotated[
        Optional[str], typer.Option(help=s.OPSQL_FILE_HELP)
    ] = s.OPSQL_FILE_DEFAULT,
):
    """
    # Unmanage Alert Resources Command
    ## This command does the following
    - Identifies the resources transitioned from unmanaged to managed due to alerts
    - Unmanage them again
    ## sample enviroment.yaml
    ```yaml
    - name: PRODurl: https://acme.api.opsramp.com
    partner: -e7f3-40cc-ed0d8f51-b117-63847a3cc9cc
    tenant: 78734cff--483f-a9ad-4495b847d70f6f91
    client_id: N3Hp43TC9UCjbu7NkYExvvkZF4SfUbtS
    client_secret: 2mKQTDwvtA4WybgMkDnWJEU6xSp5SjQjggHDD
    - name: UAT
    url: https://uat.opsramp.com
    partner: ed0d8f51--40cc-b117-63847a3cc9cc
    tenant: cc0c2a2e-9c63--9db2-ec9f6d7dbcbd
    client_id: n9PQE42zUQKFUPfZce7f39QXpczhjbJaKEdp
    client_secret: mBA3v2FjQ8xdue7f3qbHAuQxU9226xehznJj9Xu9tCjbtPmwtq3RCHTqRz68QzCj
    ```
    ### Sample opsql.json
    ```json
    {
    "objectType": "resource",
    "fields": [
        "id"
    ],
    "filterCriteria": "tags.name = \"Managed By\"  AND tags.value = \"Alert\" ",
    "pageNo": 1,
    "pageSize": 500
    }
    ```
    """

    # print(logger.getEffectiveLevel())
    opsramp_environment = OpsRampEnvironment(envname=env, envfile=env_file)
    # logger.debug("opsramp_environment: %s " % opsramp_environment)

    unmanaged_resources = CLI_Utils.do_cmd_unmanage_alert_devices_partner(
        opsramp_environment, locals()
    )

    # logger.debug("unmanaged_resources: %s " %unmanaged_resources)
    # rich.print("The Alert only resources unmanaged successfully")
    """
    The below code never gets executed
    
    if unmanaged_resources:
        rich.print("The following devices unmanaged successfully")
        rich.print(unmanaged_resources)
    """


"""
To Test
python unmanage_alert_resources.py hpe_opsramp_cli unmanage_alert_resources --help
python unmanage_alert_resources.py hpe_opsramp_cli unmanage_alert_resources --env UAT_BalaSubramanian_API

15-02-2025
Runs only when run this file from PyCharm IDE
all the environment file, json files must be there in the same folder of the this file

The following are not running
1) Running from windows terminal like below 

2) running any combination of path from terminal 
3) running from Pycharm terminal
4) running test files
"""
if __name__ == "__main__":
    app()
