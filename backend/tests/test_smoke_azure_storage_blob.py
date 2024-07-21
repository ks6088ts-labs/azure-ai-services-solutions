from logging import getLogger
from uuid import uuid4

import pytest

from backend.tests.utilities import RUN_TEST, client, image

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_storage_blob():
    path_format = "/azure_storage_blob/{0}"
    blob_name = str(uuid4())

    response = client.post(
        url=path_format.format("blobs/upload"),
        params={
            "blob_name": blob_name,
        },
        files={
            "file": (
                "test.png",
                image,
                "application/octet-stream",
            )
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.get(
        url=path_format.format("blobs"),
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.delete(
        url=path_format.format("blobs/delete"),
        params={
            "blob_name": blob_name,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")
