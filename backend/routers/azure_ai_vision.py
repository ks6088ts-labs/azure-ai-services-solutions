from logging import getLogger

from fastapi import APIRouter, UploadFile

from backend.internals import azure_ai_vision
from backend.schemas import azure_ai_vision as azure_ai_vision_schemas
from backend.settings.azure_ai_vision import Settings

logger = getLogger(__name__)
client = azure_ai_vision.AzureAiVisionClient(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_ai_vision",
    tags=["azure_ai_vision"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/image/analyze/",
    response_model=azure_ai_vision_schemas.ImageAnalysisResponse,
    status_code=200,
)
async def analyze_image(file: UploadFile):
    try:
        content = await file.read()
        result = client.analyze_image(
            image=content,
        )
    except Exception as e:
        logger.error(f"Failed to analyze image: {e}")
        raise
    return azure_ai_vision_schemas.ImageAnalysisResponse(
        result=result,
    )
