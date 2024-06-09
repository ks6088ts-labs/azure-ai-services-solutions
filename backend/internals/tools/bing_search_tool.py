from os import getenv

from dotenv import load_dotenv
from langchain_core.tools import tool

_ = load_dotenv("./settings/bing_search_tool.env")


@tool
def bing_search_tool(query: str) -> str:
    """Perform web searches by 'query' using Bing Search API. Returns search results as a string."""
    from langchain_community.utilities import BingSearchAPIWrapper

    return BingSearchAPIWrapper(
        k=int(
            getenv("BING_SEARCH_K", 1),
        ),
        bing_search_url=getenv("BING_SEARCH_URL"),
        bing_subscription_key=getenv("BING_SUBSCRIPTION_KEY"),
    ).run(
        query=query,
    )
