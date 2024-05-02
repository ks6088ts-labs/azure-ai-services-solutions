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
def frontend(
    solution_name: Annotated[str, typer.Option(help="Solution name")] = getenv("SOLUTION_NAME"),
    backend_url: Annotated[str, typer.Option(help="Backend URL")] = getenv("BACKEND_URL", "http://localhost:8000/"),
):
    from frontend.entrypoint import start

    start(
        solution_name=solution_name,
        backend_url=backend_url,
    )


if __name__ == "__main__":
    load_dotenv()
    app()
