import asyncio

import aiohttp
import streamlit as st


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
):
    st.write(f"Solution name: {solution_name}")
    if st.button("Push"):
        try:
            with st.spinner("Calling API..."):
                response = asyncio.run(http_get(url=backend_url))
            st.write(response)
        except Exception as e:
            st.write(f"Error: {e}")
