import asyncio
import logging
from os import getenv
from urllib.parse import urljoin

import streamlit as st
from dotenv import load_dotenv
from utilities import http_get

logger = logging.getLogger(__name__)
load_dotenv()


async def chat_completions_post(
    backend_url: str,
    prompt: str,
):
    from kiota_abstractions.authentication.anonymous_authentication_provider import AnonymousAuthenticationProvider
    from kiota_http.httpx_request_adapter import HttpxRequestAdapter

    from client.api_client import ApiClient
    from client.models.chat_completion_request import ChatCompletionRequest

    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(
        authentication_provider=auth_provider,
        base_url=backend_url,
    )
    client = ApiClient(request_adapter)

    response = await client.azure_openai.chat_completions.post(
        ChatCompletionRequest(
            content=prompt,
        ),
    )
    return response.content


def main(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.write("Get OpenAPI spec")
    if st.button("GET"):
        logger.info("Fetching data from backend...")
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(http_get(url=urljoin(base=urljoin(backend_url, "openapi.json"), url="")))
            st.write(response)
            logger.info("Data fetched successfully.")
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")

    st.write("---")

    st.write("Call Azure OpenAI API")
    prompt = st.text_input(
        label="Prompt",
        value="Hello",
    )
    if st.button("POST"):
        logger.info("Posting data to backend...")
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(
                    chat_completions_post(
                        backend_url=backend_url,
                        prompt=prompt,
                    )
                )
            st.write(response)
            logger.info("Data posted successfully.")
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main(
        backend_url=getenv("BACKEND_URL"),
        log_level=logging.DEBUG,
    )
