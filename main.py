import logging
import os
from typing import Annotated

import typer
from dotenv import load_dotenv


def get_log_level(debug: bool) -> int:
    return logging.DEBUG if debug else logging.INFO


def setup_logging(debug: bool = False):
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
        level=get_log_level(debug),
        force=True,
    )


app = typer.Typer()


@app.command()
def backend(
    host="0.0.0.0",
    port: Annotated[int, typer.Option(help="Port number")] = 8000,
    reload: Annotated[bool, typer.Option(help="Enable auto-reload")] = False,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from backend.entrypoint import start

    setup_logging(debug)
    start(
        host=host,
        port=port,
        log_level=get_log_level(debug),
        reload=reload,
    )


@app.command()
def frontend(
    solution_name: Annotated[str, typer.Option(help="Solution name")] = "SANDBOX",
    backend_url: Annotated[str, typer.Option(help="Backend URL")] = "http://localhost:8000/",
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    from frontend.entrypoint import start

    setup_logging(debug)
    start(
        solution_name=solution_name,
        backend_url=backend_url,
        log_level=get_log_level(debug),
    )


@app.command()
def generate_openapi_spec(
    path: Annotated[str, typer.Option(help="Output file path")] = "./specs/openapi.json",
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    import json

    from backend.fastapi import app

    setup_logging(debug)

    # create directory if not exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # generate OpenAPI spec
    with open(path, "w") as f:
        api_spec = app.openapi()
        f.write(json.dumps(api_spec, indent=2))
    logging.info(f"OpenAPI spec generated at {path}")


if __name__ == "__main__":
    load_dotenv()
    app()
