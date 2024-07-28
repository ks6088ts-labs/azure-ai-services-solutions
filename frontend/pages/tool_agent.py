import logging
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import AzureChatOpenAI
from tools.fetch_contoso_rules import fetch_contoso_rules
from tools.search_ddg import search_ddg

logger = logging.getLogger(__name__)
load_dotenv()


CUSTOM_SYSTEM_PROMPT = """
あなたは、ユーザーのリクエストに基づいてインターネットで調べ物を行うアシスタントです。
利用可能なツールを使用して、調査した情報を説明してください。
既に知っていることだけに基づいて答えないでください。回答する前にできる限り検索を行ってください。
(ユーザーが読むページを指定するなど、特別な場合は、検索する必要はありません。)

検索結果ページを見ただけでは情報があまりないと思われる場合は、次の2つのオプションを検討して試してみてください。

- 検索結果のリンクをクリックして、各ページのコンテンツにアクセスし、読んでみてください。
- 1ページが長すぎる場合は、3回以上ページ送りしないでください（メモリの負荷がかかるため）。
- 検索クエリを変更して、新しい検索を実行してください。
- 検索する内容に応じて検索に利用する言語を適切に変更してください。
- 例えば、プログラミング関連の質問については英語で検索するのがいいでしょう。

ユーザーは非常に忙しく、あなたほど自由ではありません。
そのため、ユーザーの労力を節約するために、直接的な回答を提供してください。

=== 悪い回答の例 ===
- これらのページを参照してください。
- これらのページを参照してコードを書くことができます。
- 次のページが役立つでしょう。

=== 良い回答の例 ===
- これはサンプルコードです。 -- サンプルコードをここに --
- あなたの質問の答えは -- 回答をここに --

回答の最後には、参照したページのURLを**必ず**記載してください。（これにより、ユーザーは回答を検証することができます）

ユーザーが使用している言語で回答するようにしてください。
ユーザーが日本語で質問した場合は、日本語で回答してください。ユーザーがスペイン語で質問した場合は、スペイン語で回答してください。
"""

store = {}


def wrap_with_history(runnable):
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    return RunnableWithMessageHistory(
        runnable,
        get_session_history,
        history_messages_key="chat_history",
    )


def init_page():
    st.set_page_config(page_title="Web Browsing Agent", page_icon="🤗")
    st.header("Web Browsing Agent 🤗")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Please ask me any questions you may have."}]
        st.session_state["memory"] = ConversationBufferWindowMemory(
            return_messages=True, memory_key="chat_history", k=10
        )


def create_agent():
    tools = [
        search_ddg,
        fetch_contoso_rules,
    ]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CUSTOM_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    llm = AzureChatOpenAI(
        temperature=0,
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_MODEL_CHAT"),
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=st.session_state["memory"],
    )


def main():
    init_page()
    init_messages()
    session_id = "example_session"

    web_browsing_agent = wrap_with_history(create_agent())

    for msg in st.session_state["memory"].chat_memory.messages:
        st.chat_message(msg.type).write(msg.content)

    if prompt := st.chat_input(placeholder="Type your question here..."):
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            response = web_browsing_agent.invoke(
                {"input": prompt},
                config=RunnableConfig(
                    {
                        "callbacks": [
                            st_cb,
                        ],
                        "configurable": {
                            "session_id": session_id,
                        },
                    }
                ),
            )
            st.write(response["output"])
            print(f"\chat_history:\n{store[session_id]}")


if __name__ == "__main__":
    main()
