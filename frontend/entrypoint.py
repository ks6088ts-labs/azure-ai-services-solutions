import asyncio
import logging

import aiohttp
import streamlit as st

logger = logging.getLogger(__name__)


async def http_get(url) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])
            return await response.json()


def start(
    solution_name: str,
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.write(f"Solution name: {solution_name}")
    if st.button("Push"):
        logger.info("Fetching data from backend...")
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(http_get(url=backend_url))
            st.write(response)
            logger.info("Data fetched successfully.")
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")