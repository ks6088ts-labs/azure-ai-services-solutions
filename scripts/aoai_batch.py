import json
import logging
import os
from os import getenv
from typing import Annotated

import typer
from dotenv import load_dotenv
from openai import AzureOpenAI

app = typer.Typer()


def get_log_level(debug: bool) -> int:
    return logging.DEBUG if debug else logging.INFO


def setup_logging(debug: bool = False):
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: " "%(message)s",
        level=get_log_level(debug),
        force=True,
    )


def get_azure_openai_client():
    return AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


@app.command()
def files_create(
    file: str,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    file_response = get_azure_openai_client().files.create(
        file=open(file, "rb"),
        purpose="batch",
    )
    print(file_response.model_dump_json(indent=2))


@app.command()
def files_retrieve(
    file_id: str,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    file_response = get_azure_openai_client().files.retrieve(file_id)
    print(file_response.model_dump_json(indent=2))


@app.command()
def batches_create(
    file_id: str,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    batch_response = get_azure_openai_client().batches.create(
        input_file_id=file_id,
        endpoint="/chat/completions",
        completion_window="24h",
    )

    print(batch_response.model_dump_json(indent=2))


@app.command()
def batches_retrieve(
    batch_id: str,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    batch_response = get_azure_openai_client().batches.retrieve(batch_id)
    print(batch_response.model_dump_json(indent=2))


@app.command()
def files_content(
    output_file_id: str,
    debug: Annotated[bool, typer.Option(help="Enable debug mode")] = False,
):
    setup_logging(debug)

    file_response = get_azure_openai_client().files.content(output_file_id)
    raw_responses = file_response.text.strip().split("\n")

    for raw_response in raw_responses:
        json_response = json.loads(raw_response)
        formatted_json = json.dumps(json_response, indent=2)
        print(formatted_json)


if __name__ == "__main__":
    """
    Python script to interact with Azure OpenAI API for batch processing.

    # Help
    poetry run python scripts/aoai_batch.py --help
    # Upload batch file
    poetry run python scripts/aoai_batch.py files-create ./scripts/test.jsonl
    # Track file upload status
    poetry run python scripts/aoai_batch.py files-retrieve <file_id>
    # Wait for upload status to be `processed`
    # Create batch job
    poetry run python scripts/aoai_batch.py batches-create <file_id>
    # Track batch job progress
    poetry run python scripts/aoai_batch.py batches-retrieve <batch_id>
    # Wait for batch job progress to be `processed`
    # Retrieve batch job output file
    poetry run python scripts/aoai_batch.py files-content <output_file_id>
    """
    load_dotenv()
    app()
