"""Snowboard package."""

from __future__ import annotations

import typer
from gunicorn.app.wsgiapp import WSGIApplication
from typing_extensions import Annotated

cli = typer.Typer()


class StandaloneApplication(WSGIApplication):
    """Run a Gunicorn Application."""

    def __init__(self, app_uri: str, options: dict) -> None:
        """Initialize the Standalone Application Class."""
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self) -> None:
        """Load Gunicorn Configuration."""
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


@cli.command()
def main(
    debug: Annotated[bool, typer.Option(help="Run the Flask Debug Server")] = False,  # noqa: FBT002
    host: Annotated[str, typer.Option(help="Host to run on")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Port to run on")] = 6502,
) -> None:
    """Snowboard CLI."""
    if debug:
        from snowboard.dashboard import app

        app.run_server(debug=debug, host=host, port=port)
    else:
        StandaloneApplication(
            "snowboard.dashboard:server",
            options={"bind": f"{host}:{port}", "accesslog": "-", "errorlog": "-"},
        ).run()


if __name__ == "__main__":
    cli()
