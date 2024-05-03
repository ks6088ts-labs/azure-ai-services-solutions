from logging import getLogger

from fastapi import APIRouter, UploadFile

from backend.internals import document_intelligence
from backend.schemas import document_intelligence as document_intelligence_schemas

logger = getLogger(__name__)

router = APIRouter(
    prefix="/document_intelligence",
    tags=["document_intelligence"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/analyze_document/",
    response_model=document_intelligence_schemas.AnalyzeDocumentResponse,
    status_code=200,
)
async def analyze_document(file: UploadFile):
    try:
        content = await file.read()
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        raise
    return document_intelligence.analyze_document(
        body=document_intelligence_schemas.AnalyzeDocumentRequest(
            content=content,
        )
    )
