from logging import getLogger

import pytest

from tests.utilities import RUN_TEST, client, image

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_ai_document_intelligence():
    path_format = "/azure_ai_document_intelligence/{0}"
    response = client.post(
        url=path_format.format("analyze_document"),
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
