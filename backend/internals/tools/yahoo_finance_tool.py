from langchain_core.tools import tool


@tool
def yahoo_finance_tool(query: str) -> str:
    """Perform searches for financial news on Yahoo Finance by 'query' which is a company ticker to look up.
    For example, AAPL for Apple, MSFT for Microsoft.
    """
    from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

    return YahooFinanceNewsTool().run(query)
