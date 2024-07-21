from logging import getLogger
from uuid import uuid4

import pytest

from .utilities import RUN_TEST, client

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_cosmos_db():
    path_format = "/azure_cosmos_db/{0}"
    database_id = str(uuid4())
    container_id = str(uuid4())

    response = client.post(
        url=path_format.format("database"),
        json={
            "database_id": database_id,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.post(
        url=path_format.format("container"),
        json={
            "database_id": database_id,
            "container_id": container_id,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.post(
        url=path_format.format("item"),
        json={
            "database_id": database_id,
            "container_id": container_id,
            "item": {
                "id": str(uuid4()),
                "name": "test",
            },
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")
