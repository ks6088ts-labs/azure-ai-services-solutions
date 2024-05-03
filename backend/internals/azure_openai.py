from logging import getLogger

from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

from backend.schemas import azure_openai as azure_openai_schemas
from backend.settings import azure_openai as azure_openai_settings

logger = getLogger(__name__)

settings = azure_openai_settings.Settings()


def create_chat_completions(
    body: azure_openai_schemas.ChatCompletionRequest,
) -> azure_openai_schemas.ChatCompletionResponse:
    client = AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )
    response: ChatCompletion = client.chat.completions.create(
        model=settings.azure_openai_gpt_model,
        messages=[
            {
                "role": "user",
                "content": body.content,
            },
        ],
        stream=body.stream,
    )
    logger.info(response)
    return azure_openai_schemas.ChatCompletionResponse(
        content=response.choices[0].message.content,
    )
