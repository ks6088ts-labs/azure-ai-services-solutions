from logging import getLogger

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult, ContentFormat
from azure.core.credentials import AzureKeyCredential
from settings.azure_ai_document_intelligence import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_document_intelligence_client(self) -> DocumentIntelligenceClient:
        return DocumentIntelligenceClient(
            endpoint=self.settings.azure_ai_document_intelligence_endpoint,
            credential=AzureKeyCredential(self.settings.azure_ai_document_intelligence_api_key),
        )

    def analyze_document(
        self,
        bytes_source: bytes,
    ) -> AnalyzeResult:
        client = self.get_document_intelligence_client()
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            analyze_request=AnalyzeDocumentRequest(
                bytes_source=bytes_source,
            ),
            output_content_format=ContentFormat.MARKDOWN,
        )
        result = poller.result()
        logger.info(result)
        return result
