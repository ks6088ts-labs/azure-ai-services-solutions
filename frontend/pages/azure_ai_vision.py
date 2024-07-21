import asyncio
import logging
from io import BytesIO
from urllib.parse import urljoin

import streamlit as st
from utilities import http_post_file

logger = logging.getLogger(__name__)


def main(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.header("Azure AI Vision")

    file_uploader = st.file_uploader(
        label="Choose a file",
        key="file_uploader",
    )

    analyze_button = st.button(
        label="Analyze",
        key="analyze_button",
    )

    if file_uploader is not None:
        st.image(file_uploader, caption="Uploaded image")
        if analyze_button:
            with st.spinner("Analyzing..."):
                bytes_data = file_uploader.getvalue()
                response = asyncio.run(
                    http_post_file(
                        url=urljoin(base=backend_url, url="/azure_ai_vision/image/analyze"),
                        data_bytes_io=BytesIO(bytes_data),
                    )
                )
                st.write(response)
    else:
        st.warning("Please upload a file first")


if __name__ == "__main__":
    main(
        backend_url="http://localhost:8000",
        log_level=logging.DEBUG,
    )
