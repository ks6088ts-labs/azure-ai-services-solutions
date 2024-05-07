from logging import getLogger

from fastapi import APIRouter, UploadFile

from backend.internals import azure_openai
from backend.schemas import azure_openai as azure_openai_schemas
from backend.settings.azure_openai import Settings

logger = getLogger(__name__)
client = azure_openai.Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_openai",
    tags=["azure_openai"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/chat_completions/",
    response_model=azure_openai_schemas.ChatCompletionResponse,
    status_code=200,
)
async def create_chat_completions(body: azure_openai_schemas.ChatCompletionRequest):
    response = client.create_chat_completions(
        content=body.content,
        stream=body.stream,
    )
    return azure_openai_schemas.ChatCompletionResponse(
        content=response.choices[0].message.content,
    )


@router.post(
    "/chat_completions_with_vision/",
    response_model=azure_openai_schemas.ChatCompletionWithVisionResponse,
    status_code=200,
)
async def create_chat_completions_with_vision(
    file: UploadFile,
    system_prompt: str = "You are a helpful assistant.",
    user_prompt: str = "Please explain the attached image.",
):
    try:
        image = await file.read()
        response = client.create_chat_completions_with_vision(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image=image,
        )
    except Exception as e:
        logger.error(f"Failed to create chat completions with vision: {e}")
        raise
    return azure_openai_schemas.ChatCompletionWithVisionResponse(
        content=response.choices[0].message.content,
    )
