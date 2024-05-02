from logging import getLogger
from os import getenv

from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

logger = getLogger(__name__)


def create_chat_completion(content: str, stream: bool):
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )
    response: ChatCompletion = client.chat.completions.create(
        model=getenv("AZURE_OPENAI_MODEL_GPT"),
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
        stream=stream,
    )
    logger.info(response)
    return response.choices[0].message.content
