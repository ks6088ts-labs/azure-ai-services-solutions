from logging import getLogger

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from backend.settings.azure_ai_vision import Settings

logger = getLogger(__name__)


class AzureAiVisionClient:
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
                VisualFeatures.CAPTION,
                VisualFeatures.READ,
            ],
        )
        logger.info("Analyzed image")
        return result.as_dict()
