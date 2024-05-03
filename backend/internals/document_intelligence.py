from logging import getLogger

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential

from backend.schemas import document_intelligence as document_intelligence_schemas
from backend.settings import document_intelligence as document_intelligence_settings

logger = getLogger(__name__)

settings = document_intelligence_settings.Settings()


def analyze_document(
    body: document_intelligence_schemas.AnalyzeDocumentRequest,
) -> document_intelligence_schemas.AnalyzeDocumentResponse:
    client = DocumentIntelligenceClient(
        endpoint=settings.document_intelligence_endpoint,
        credential=AzureKeyCredential(settings.document_intelligence_api_key),
    )
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        analyze_request=AnalyzeDocumentRequest(
            bytes_source=body.content,
        ),
        output_content_format=ContentFormat.MARKDOWN,
    )
    result = poller.result()
    logger.info(result)
    return document_intelligence_schemas.AnalyzeDocumentResponse(
        content=result.content,
    )
