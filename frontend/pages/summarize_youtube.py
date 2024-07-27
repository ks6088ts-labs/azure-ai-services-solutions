import logging
import traceback
from os import getenv
from urllib.parse import urlparse

import streamlit as st
import tiktoken
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader  # Youtube用
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import AzureChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)
load_dotenv()


SUMMARIZE_PROMPT = """Please provide a clear 300 word summary of the following content in Japanese.

========

{content}

========
"""


def init_page():
    st.set_page_config(page_title="Summarize YouTube", page_icon="💻")
    st.header("Summarize YouTube")
    st.sidebar.title("Options")


def select_model(temperature=0):
    return AzureChatOpenAI(
        temperature=temperature,
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        model=getenv("AZURE_OPENAI_MODEL_CHAT"),
    )


def init_summarize_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("user", SUMMARIZE_PROMPT),
        ]
    )
    output_parser = StrOutputParser()
    return prompt | llm | output_parser


def init_map_reduce_chain():
    summarize_chain = init_summarize_chain()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o",  # hard-coded for now
        chunk_size=16000,
        chunk_overlap=0,
    )
    text_split = RunnableLambda(lambda x: [{"content": doc} for doc in text_splitter.split_text(x["content"])])
    text_concat = RunnableLambda(lambda x: {"content": "\n".join(x)})
    return text_split | summarize_chain.map() | text_concat | summarize_chain


def init_chain():
    summarize_chain = init_summarize_chain()
    map_reduce_chain = init_map_reduce_chain()

    def route(x):
        encoding = tiktoken.encoding_for_model("gpt-4o")
        token_count = len(encoding.encode(x["content"]))
        if token_count > 16000:
            return map_reduce_chain
        else:
            return summarize_chain

    chain = RunnableLambda(route)

    return chain


def validate_url(url):
    """URLが有効かどうかを判定する関数"""
    try:
        result = urlparse(url)
        if result.netloc != "www.youtube.com":
            return False
        if not result.path.startswith("/watch"):
            return False
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    with st.spinner("Fetching Youtube ..."):
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=True,  # タイトルや再生数も取得できる
            language=["en", "ja"],  # 英語→日本語の優先順位で字幕を取得
        )
        res = loader.load()  # list of `Document` (page_content, metadata)
        try:
            if res:
                content = res[0].page_content
                title = res[0].metadata["title"]
                return f"Title: {title}\n\n{content}"
            else:
                return None
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            st.write(traceback.format_exc())
            return None


def main():
    init_page()
    chain = init_chain()
    if url := st.text_input("URL: ", key="input"):
        # clear text input
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.write("Please input valid url")
        else:
            if content := get_content(url):
                st.markdown("## Summary")
                st.write_stream(chain.stream({"content": content}))
                st.markdown("---")
                st.markdown("## Original Text")
                st.write(content)


if __name__ == "__main__":
    main()
