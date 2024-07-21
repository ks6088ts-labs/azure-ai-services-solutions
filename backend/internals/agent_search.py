from logging import getLogger
from os import environ

from internals.agents.basic import Agent
from internals.tools.bing_search_tool import bing_search_tool
from internals.tools.utility_tool import (
    add,
    exponentiate,
    get_date_diffs,
    get_date_from_offset,
    get_datetime_today,
    multiply,
)
from internals.tools.yahoo_finance_tool import yahoo_finance_tool
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from settings.agents import Settings

logger = getLogger(__name__)


def create_tools():
    return [
        bing_search_tool,
        add,
        exponentiate,
        get_date_diffs,
        get_datetime_today,
        get_date_from_offset,
        multiply,
        yahoo_finance_tool,
    ]


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        # https://python.langchain.com/v0.1/docs/langsmith/walkthrough/#log-runs-to-langsmith
        environ["LANGCHAIN_TRACING_V2"] = settings.agents_langchain_tracing_v2
        environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        environ["LANGCHAIN_API_KEY"] = settings.agents_langchain_api_key

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
