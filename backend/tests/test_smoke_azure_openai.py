from logging import getLogger

import pytest

from .utilities import RUN_TEST, client, image

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_openai_chat_completions():
    path_format = "/azure_openai/{0}"

    response = client.post(
        url=path_format.format("chat_completions"),
        json={
            "content": "Hello, how are you?",
            "stream": False,
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_openai_chat_completions_with_vision():
    path_format = "/azure_openai/{0}"
    response = client.post(
        url=path_format.format("chat_completions_with_vision"),
        params={
            "system_prompt": "You are a helpful assistant.",
            "user_prompt": "Please explain the attached image.",
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
