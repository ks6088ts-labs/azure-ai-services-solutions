from logging import getLogger
from uuid import uuid4

import pytest
from tests.utilities import RUN_TEST, client

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_storage_queue():
    path_format = "/azure_storage_queue/{0}"
    queue_name = str(uuid4())

    response = client.post(
        url=path_format.format("queues"),
        json={
            "queue_name": queue_name,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.post(
        url=path_format.format("messages"),
        json={
            "queue_name": queue_name,
            "message": "hello",
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.get(
        url=path_format.format("messages"),
        params={
            "queue_name": queue_name,
            "max_messages": 1,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")

    response = client.delete(
        url=path_format.format(f"queues/{queue_name}"),
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")
