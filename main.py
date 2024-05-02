from os import getenv
from typing import Annotated

import typer
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def backend(
    host="0.0.0.0",
    port: Annotated[int, typer.Option(help="Port number")] = 8000,
    log_level="info",
    reload: Annotated[bool, typer.Option(help="Enable auto-reload")] = False,
):
    from backend.entrypoint import start

    start(
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@app.command()
def frontend():
    print(f"Hello {getenv('APPLICATION_NAME')}")


if __name__ == "__main__":
    load_dotenv()
    app()
