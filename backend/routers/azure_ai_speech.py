from logging import getLogger

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from internals.azure_ai_speech import Client
from schemas import azure_ai_speech as azure_ai_speech_schemas

from settings.azure_ai_speech import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_ai_speech",
    tags=["azure_ai_speech"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/transcriptions",
    response_model=azure_ai_speech_schemas.CreateTranscriptionResponse,
    status_code=200,
)
async def create_transcription(request: azure_ai_speech_schemas.CreateTranscriptionRequest):
    transcription_id = client.create_transcription(
        content_url=request.content_url,
        locale=request.locale,
    )
    return azure_ai_speech_schemas.CreateTranscriptionResponse(
        transcription_id=transcription_id,
    )


@router.get(
    "/transcriptions/{transcription_id}",
    status_code=200,
)
async def get_transcription(transcription_id: str):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=client.get_transcription(
            transcription_id=transcription_id,
        ),
    )


@router.get(
    "/transcriptions/{transcription_id}/files",
    status_code=200,
)
async def get_transcription_files(transcription_id: str):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=client.get_transcription_files(
            transcription_id=transcription_id,
        ),
    )
