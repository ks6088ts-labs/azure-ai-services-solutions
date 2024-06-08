from logging import getLogger

import pytest

from tests.utilities import RUN_TEST, client

logger = getLogger(__name__)


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_ai_speech_create_transcription():
    path_format = "/azure_ai_speech/{0}"
    response = client.post(
        url=path_format.format("transcriptions"),
        json={
            "content_url": "https://<blob_account_name>.blob.core.windows.net/<blob_container_name>/<blob_name>",
            "locale": "ja-JP",
        },
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")


@pytest.mark.skipif(RUN_TEST, reason="need to launch the backend server first")
def test_azure_ai_speech_get_transcription():
    path_format = "/azure_ai_speech/{0}"
    transcription_id = "<transcription_id>"
    response = client.get(
        url=path_format.format(f"transcriptions/{transcription_id}"),
    )
    assert response.status_code == 200
    logger.info(f"response: {response.json()}")
