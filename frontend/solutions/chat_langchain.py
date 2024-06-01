import logging
from os import getenv
from uuid import uuid4

import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI

logger = logging.getLogger(__name__)
load_dotenv("frontend.env")
store = {}
config = {"configurable": {"session_id": str(uuid4())}}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def start(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.title("ChatGPT-like clone implemented with LangChain")

    model = AzureChatOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=getenv("AZURE_OPENAI_GPT_MODEL"),
    )

    with_message_history = RunnableWithMessageHistory(
        runnable=model,
        get_session_history=get_session_history,
        # input_messages_key="input",
        # history_messages_key="history",
    )

    chat_message_history = with_message_history.get_session_history(
        session_id=config["configurable"]["session_id"],
    )
    for message in chat_message_history.messages:
        with st.chat_message(message.type):
            st.markdown(message.content)

    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = with_message_history.invoke(
                [HumanMessage(content=prompt)],
                config=config,
            )

            st.markdown(response.content)
