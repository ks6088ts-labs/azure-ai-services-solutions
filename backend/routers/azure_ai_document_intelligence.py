from logging import getLogger

from fastapi import APIRouter, UploadFile
from internals.azure_ai_document_intelligence import Client
from schemas import azure_ai_document_intelligence as azure_ai_document_intelligence_schemas

from settings.azure_ai_document_intelligence import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_ai_document_intelligence",
    tags=["azure_ai_document_intelligence"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/analyze_document",
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
