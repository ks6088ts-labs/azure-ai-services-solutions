from os import getenv

import requests
from fastapi.testclient import TestClient

from backend.fastapi import app
from main import setup_logging

setup_logging(debug=True)

client = TestClient(
    app=app,
)
image = requests.get(
    url="https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/documentintelligence/azure-ai-documentintelligence/tests/sample_forms/receipt/contoso-receipt.png",
).content
RUN_TEST = getenv("RUN_TEST", "True") == "True"
