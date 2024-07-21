from logging import getLogger

import pytest

from .utilities import RUN_TEST, client

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_event_grid():
    path_format = "/azure_event_grid/{0}"
    response = client.post(
        url=path_format.format("event_grid_event"),
        json={
            "data": {
                "team": "azure-sdk",
            },
            "subject": "Door1",
            "event_type": "Azure.Sdk.Demo",
            "data_version": "2.0",
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")
