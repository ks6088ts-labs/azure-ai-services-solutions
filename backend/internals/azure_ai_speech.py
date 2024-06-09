from logging import getLogger
from urllib.parse import urljoin

import requests

from backend.settings.azure_ai_speech import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create_transcription(
        self,
        content_url: str,
        locale: str,
    ) -> str:
        response = requests.post(
            url=urljoin(
                self.settings.azure_ai_speech_endpoint,
                "speechtotext/v3.2-preview.2/transcriptions",
            ),
            headers={
                "Ocp-Apim-Subscription-Key": self.settings.azure_ai_speech_api_key,
                "Content-Type": "application/json",
            },
            json={
                "contentUrls": [
                    content_url,
                ],
                "locale": locale,
                "displayName": "My Transcription",
                "model": {
                    # FIXME: remove the hardcoded model
                    "self": urljoin(
                        urljoin(
                            self.settings.azure_ai_speech_endpoint,
                            "speechtotext/v3.2-preview.2/models/base",
                        ),
                        "e418c4a9-9937-4db7-b2c9-8afbff72d950",
                    ),
                },
                "properties": {
                    "diarizationEnabled": False,
                    "displayFormWordLevelTimestampsEnabled": False,
                    "wordLevelTimestampsEnabled": False,
                    "profanityFilterMode": "Masked",
                    "punctuationMode": "DictatedAndAutomatic",
                    "timeToLive": "PT24H",  # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/batch-transcription-create?pivots=rest-api
                },
            },
        )
        result = response.json()
        print(result)
        return result["self"].split("/")[-1]

    def get_transcription(
        self,
        transcription_id: str,
    ) -> str:
        return requests.get(
            url=urljoin(
                self.settings.azure_ai_speech_endpoint,
                urljoin("speechtotext/v3.2-preview.2/", f"transcriptions/{transcription_id}"),
            ),
            headers={
                "Ocp-Apim-Subscription-Key": self.settings.azure_ai_speech_api_key,
            },
        ).json()

    def get_transcription_files(
        self,
        transcription_id: str,
    ):
        return requests.get(
            url=urljoin(
                self.settings.azure_ai_speech_endpoint,
                urljoin("speechtotext/v3.2-preview.2/", f"transcriptions/{transcription_id}/files"),
            ),
            headers={
                "Ocp-Apim-Subscription-Key": self.settings.azure_ai_speech_api_key,
            },
        ).json()
