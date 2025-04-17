import typer
from pinger.app import app
from pinger.cli.app.cd.struct import cd_app
from pinger.cli.app.env.struct import env_app
from pinger.cli.app.secrets.struct import secrets_app

app_sub = typer.Typer(no_args_is_help=True)
app_sub.add_typer(cd_app, name="cd", help="manage deployments")
app_sub.add_typer(env_app, name="env", help="manage environments")
app_sub.add_typer(secrets_app, name="secrets", help="manage secrets")


@app_sub.command("start")
def start():
    """
    start local development environment.
    """
    app().start()


@app_sub.command("restart")
def restart():
    """
    restart containers.
    """
    app().restart()


@app_sub.command("shell")
def shell():
    """
    Drop into a bash shell in the 'main' container, creating and starting it if necessary.
    """
    app().shell()


@app_sub.command("ci")
def ci():
    """
    build the application artifact

    Example:
        pinger app ci
    """
    app().ci()


@app_sub.command("scale")
def scale(
    env: str = typer.Argument(..., help="environment name"),
    count: int = typer.Argument(..., help="count to scale to"),
):
    """
    scale a service to a node or task count
    """
    app().scale(env, count)
