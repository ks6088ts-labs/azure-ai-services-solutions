import logging
import os
from typing import Annotated

import typer
from dotenv import load_dotenv

debug = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]
log_level = logging.DEBUG if debug else logging.INFO

logging.basicConfig(
    format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
    level=log_level,
    force=True,
)

app = typer.Typer()


@app.command()
def backend(
    host="0.0.0.0",
    port: Annotated[int, typer.Option(help="Port number")] = 8000,
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
    solution_name: Annotated[str, typer.Option(help="Solution name")] = os.getenv("SOLUTION_NAME"),
    backend_url: Annotated[str, typer.Option(help="Backend URL")] = os.getenv("BACKEND_URL", "http://localhost:8000/"),
):
    from frontend.entrypoint import start
    from frontend.solutions.types import SolutionType

    # convert solution_name to SolutionType
    try:
        solution_type = SolutionType(solution_name.upper())
    except ValueError:
        typer.echo(f"Invalid solution name: {solution_name}", err=True)
        raise typer.Exit(code=1)

    start(
        solution_type=solution_type,
        backend_url=backend_url,
        log_level=log_level,
    )


if __name__ == "__main__":
    load_dotenv()
    app()
