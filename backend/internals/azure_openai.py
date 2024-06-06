from base64 import b64encode
from collections.abc import AsyncIterable
from logging import getLogger

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

from backend.settings.azure_openai import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_client(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            api_key=self.settings.azure_openai_api_key,
            api_version=self.settings.azure_openai_api_version,
            azure_endpoint=self.settings.azure_openai_endpoint,
            azure_deployment=self.settings.azure_openai_gpt_model,
        )

    def create_chat_completions(
        self,
        content: str,
    ) -> str:
        response = self.get_client().invoke(
            [
                HumanMessage(
                    content=content,
                ),
            ]
        )
        logger.info(response)
        return response.content

    async def create_chat_completions_stream(
        self,
        content: str,
    ) -> AsyncIterable[str]:
        llm = self.get_client()
        messages = [HumanMessagePromptTemplate.from_template(template="{message}")]
        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm
        res = chain.astream({"message": content})
        async for msg in res:
            logger.info(msg)
            yield msg.content

    def create_chat_completions_with_vision(
        self,
        system_prompt: str,
        user_prompt: str,
        image: bytes,
    ) -> str:
        encoded_image = b64encode(image).decode("ascii")

        response = self.get_client().invoke(
            [
                SystemMessage(
                    content=system_prompt,
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": user_prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                        },
                    ],
                ),
            ]
        )
        logger.info(response)
        return response.content
