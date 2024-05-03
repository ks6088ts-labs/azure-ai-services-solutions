import asyncio
import logging
from urllib.parse import urljoin

import streamlit as st

from backend.schemas import azure_openai as azure_openai_schemas  # FIXME: remove dependency on backend
from frontend.solutions.utilities import http_get, http_post

logger = logging.getLogger(__name__)


def start(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.write("Misc solution")

    # GET
    if st.button("GET"):
        logger.info("Fetching data from backend...")
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(http_get(url=urljoin(base=backend_url, url="")))
            st.write(response)
            logger.info("Data fetched successfully.")
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")

    st.write("---")

    # POST
    prompt = st.text_input(
        label="Prompt",
        value="Hello",
    )
    if st.button("POST"):
        logger.info("Posting data to backend...")
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(
                    http_post(
                        url=urljoin(base=backend_url, url="/azure_openai/chat_completions/"),
                        data=azure_openai_schemas.ChatCompletionRequest(
                            content=prompt,
                            stream=False,
                        ).model_dump(),
                    )
                )
            st.write(response)
            logger.info("Data posted successfully.")
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")
