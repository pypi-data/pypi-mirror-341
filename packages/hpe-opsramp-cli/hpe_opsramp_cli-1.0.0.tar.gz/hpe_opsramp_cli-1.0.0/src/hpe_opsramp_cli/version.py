import typer

version_app = typer.Typer()


@version_app.command()
def version():
    """
    This command prints the *version* of *HPE OpsRamp CLI*
    """
    print(f"HPE OpsRamp CLI Version is 1.0.0")
