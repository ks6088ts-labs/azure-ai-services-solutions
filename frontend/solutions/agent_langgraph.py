import logging
import operator
from collections.abc import Sequence
from os import getenv
from typing import Annotated, TypedDict

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.runnables import ConfigurableField, RunnableLambda
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, StateGraph

from frontend.solutions.internals.tools.bing_search import bing_search_tool
from frontend.solutions.internals.tools.examples import (
    add,
    exponentiate,
    get_date_diffs,
    get_date_from_offset,
    get_datetime_today,
    multiply,
)

logger = logging.getLogger(__name__)
load_dotenv("frontend.env")

tools = [
    multiply,
    exponentiate,
    add,
    get_date_diffs,
    get_datetime_today,
    get_date_from_offset,
    bing_search_tool,
]
llm = AzureChatOpenAI(
    api_key=getenv("AZURE_OPENAI_API_KEY"),
    api_version=getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=getenv("AZURE_OPENAI_GPT_MODEL"),
).bind_tools(tools)

llm_with_tools = llm.configurable_alternatives(
    ConfigurableField(id="llm"),
)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def should_continue(state):
    return "continue" if state["messages"][-1].tool_calls else "end"


def call_model(state, config):
    return {"messages": [llm_with_tools.invoke(state["messages"], config=config)]}


def call_tools(state):
    def _invoke_tool(tool_call):
        tool = {tool.name: tool for tool in tools}[tool_call["name"]]
        return ToolMessage(tool.invoke(tool_call["args"]), tool_call_id=tool_call["id"])

    tool_executor = RunnableLambda(_invoke_tool)
    last_message = state["messages"][-1]
    return {"messages": tool_executor.batch(last_message.tool_calls)}


def create_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("action", call_tools)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )
    workflow.add_edge("action", "agent")
    return workflow.compile()


def start(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.title("ChatGPT-like clone")

    graph = create_graph()

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Analyzing..."):
            with st.chat_message("assistant"):
                response = graph.invoke(
                    {
                        "messages": [
                            HumanMessage(prompt),
                        ]
                    }
                )
                st.json(response)
