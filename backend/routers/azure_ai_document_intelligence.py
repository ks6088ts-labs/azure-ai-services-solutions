from logging import getLogger

from fastapi import APIRouter, UploadFile

from backend.internals import azure_ai_document_intelligence
from backend.schemas import azure_ai_document_intelligence as azure_ai_document_intelligence_schemas
from backend.settings.azure_ai_document_intelligence import Settings

logger = getLogger(__name__)
client = azure_ai_document_intelligence.AzureAiDocumentIntelligenceClient(
    settings=Settings(),
)
router = APIRouter(
    prefix="/azure_ai_document_intelligence",
    tags=["azure_ai_document_intelligence"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/analyze_document/",
    response_model=azure_ai_document_intelligence_schemas.AnalyzeDocumentResponse,
    status_code=200,
)
async def analyze_document(file: UploadFile):
    try:
        content = await file.read()
        result = client.analyze_document(
            bytes_source=content,
        )
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        raise
    return azure_ai_document_intelligence_schemas.AnalyzeDocumentResponse(
        content=result.content,
    )
