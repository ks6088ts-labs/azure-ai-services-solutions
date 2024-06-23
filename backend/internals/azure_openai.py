from base64 import b64encode
from collections.abc import AsyncIterable
from logging import getLogger

from openai import AzureOpenAI

from backend.settings.azure_openai import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
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
    ) -> str:
        response = self.get_client().chat.completions.create(
            model=self.settings.azure_openai_gpt_model,
            messages=[
                {"role": "user", "content": content},
            ],
            stream=False,
        )
        logger.info(response)
        return response.choices[0].message.content

    async def create_chat_completions_stream(
        self,
        content: str,
    ) -> AsyncIterable[str]:
        _ = self.get_client().chat.completions.create(
            model=self.settings.azure_openai_gpt_model,
            messages=[
                {"role": "user", "content": content},
            ],
            stream=True,
        )
        assert False, "Yet to be implemented."

    def create_chat_completions_with_vision(
        self,
        system_prompt: str,
        user_prompt: str,
        image: bytes,
    ) -> str:
        encoded_image = b64encode(image).decode("ascii")

        response = self.get_client().chat.completions.create(
            model=self.settings.azure_openai_gpt_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                    ],
                },
            ],
            stream=False,
        )
        logger.info(response)
        return response.choices[0].message.content
