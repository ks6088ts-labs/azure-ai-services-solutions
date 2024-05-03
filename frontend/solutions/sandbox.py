import asyncio
import logging
from urllib.parse import urljoin

import aiohttp
import streamlit as st

from backend.schemas import azure_openai as azure_openai_schemas

logger = logging.getLogger(__name__)


async def http_get(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def http_post(url: str, data: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url,
            json=data,
        ) as response:
            response.raise_for_status()
            return await response.json()


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
