import logging
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

logger = logging.getLogger(__name__)
load_dotenv()


def main(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.title("ChatGPT-like clone")

    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = client.chat.completions.create(
            model=getenv("AZURE_OPENAI_MODEL_CHAT"),
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        with st.chat_message("assistant", avatar="assistant"):
            placeholder = st.empty()
            assistant_text = ""
            for chunk in response:
                if len(chunk.choices) <= 0:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    assistant_text += content
                    placeholder.write(assistant_text)
            st.session_state.messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    main(
        backend_url=getenv("BACKEND_URL"),
        log_level=logging.DEBUG,
    )
