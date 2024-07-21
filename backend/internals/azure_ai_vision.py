from logging import getLogger

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from settings.azure_ai_vision import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_image_analysis_client(self) -> ImageAnalysisClient:
        return ImageAnalysisClient(
            endpoint=self.settings.azure_ai_vision_endpoint,
            credential=AzureKeyCredential(self.settings.azure_ai_vision_api_key),
        )

    def analyze_image(
        self,
        image: bytes,
    ) -> dict:
        image_analysis_client = self.get_image_analysis_client()
        result = image_analysis_client.analyze(
            image_data=image,
            visual_features=[
                VisualFeatures.READ,
            ],
        )
        logger.info("Analyzed image")
        return result.as_dict()

    def vectorize_image(
        self,
        image: bytes,
    ) -> dict:
        # FIXME: replace with Azure SDK when available
        from urllib.parse import urljoin

        import requests

        url = urljoin(
            self.settings.azure_ai_vision_endpoint,
            "/computervision/retrieval:vectorizeImage",
        )
        params = {
            "overload": "stream",
            "api-version": "2023-02-01-preview",
            "modelVersion": "latest",
        }
        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": self.settings.azure_ai_vision_api_key,
        }
        response = requests.post(
            url=url,
            params=params,
            headers=headers,
            data=image,
        )
        response.raise_for_status()
        return response.json()
