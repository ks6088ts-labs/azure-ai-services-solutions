from logging import getLogger

from fastapi import APIRouter

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
