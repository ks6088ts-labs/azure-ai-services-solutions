from logging import getLogger

import pytest

from tests.utilities import RUN_TEST, client, image

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_ai_vision_image_analyze():
    path_format = "/azure_ai_vision/{0}"
    response = client.post(
        url=path_format.format("image/analyze"),
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


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_ai_vision_image_vectorize():
    path_format = "/azure_ai_vision/{0}"
    response = client.post(
        url=path_format.format("image/vectorize"),
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
