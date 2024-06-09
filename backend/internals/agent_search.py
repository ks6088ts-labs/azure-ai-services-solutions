from logging import getLogger

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from backend.internals.agents.basic import Agent
from backend.internals.tools.bing_search_tool import bing_search_tool
from backend.settings.agents import Settings

logger = getLogger(__name__)


def create_tools():
    return [
        bing_search_tool,
    ]


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
    ):
        agent = Agent(
            tools=create_tools(),
            model=AzureChatOpenAI(
                api_key=self.settings.agents_azure_openai_api_key,
                api_version=self.settings.agents_azure_openai_api_version,
                azure_endpoint=self.settings.agents_azure_openai_endpoint,
                azure_deployment=self.settings.agents_azure_openai_gpt_model,
            ).bind_tools(create_tools()),
            system=system_prompt,
        )
        return agent.graph.invoke(
            {
                "messages": [HumanMessage(content=user_prompt)],
            }
        )
