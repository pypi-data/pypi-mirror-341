import typer
from typing_extensions import Annotated
from typing import Optional

from .unmanage_alert_resources import opsramp_cli_app as unmanage_alert_resources_app
from hpe_opsramp_cli.version import version_app as version_app
from hpe_opsramp_cli.singleton_logger import SingletonLogger


from . import settings as s

app = typer.Typer(rich_markup_mode="markdown")
app.add_typer(unmanage_alert_resources_app)
app.add_typer(version_app)


def setup_logging(log_level: str):
    SingletonLogger().get_logger(log_level=log_level)


@app.callback()
def main(
    log_level: Annotated[
        Optional[str], typer.Option(help=s.LOG_LEVEL_HELP)
    ] = s.LOG_LEVEL_DEFAULT,
):
    setup_logging(log_level)


"""
opsramp_cli_app = typer.Typer()
app.add_typer(opsramp_cli_app, name=PARENT_COMMAND)
"""

if __name__ == "__main__":
    app()
