import os
import sys
from os import getenv

import requests

# FIXME: This is a workaround to import the FastAPI app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from core import app
from fastapi.testclient import TestClient
from main import setup_logging

setup_logging(debug=True)

client = TestClient(
    app=app,
)
image = requests.get(
    url="https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/sdk/documentintelligence/azure-ai-documentintelligence/tests/sample_forms/receipt/contoso-receipt.png",
).content
RUN_TEST = getenv("RUN_TEST", "True") == "True"
