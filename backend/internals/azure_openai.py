from logging import getLogger

from openai import AzureOpenAI
from openai.types.chat import ChatCompletion

from backend.settings import azure_openai as azure_openai_settings

logger = getLogger(__name__)

settings = azure_openai_settings.Settings()


class Client:
    def __init__(self, settings: azure_openai_settings.Settings) -> None:
        self.settings = settings

    def get_client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            azure_endpoint=self.settings.azure_openai_endpoint,
        )

    def create_chat_completions(
        self,
        content: str,
        stream: bool = False,
    ) -> ChatCompletion:
        client = self.get_client()
        response: ChatCompletion = client.chat.completions.create(
            model=self.settings.azure_openai_gpt_model,
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
            ],
            stream=stream,
        )
        logger.info(response)
        return response
