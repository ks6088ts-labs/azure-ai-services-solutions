import asyncio
import logging
from io import BytesIO
from os import getenv
from urllib.parse import urljoin

import streamlit as st
from dotenv import load_dotenv
from utilities import http_post_file

logger = logging.getLogger(__name__)
load_dotenv()


def main(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.header("Document Intelligence")

    file_uploader = st.file_uploader(
        label="Choose a file",
        key="document_intelligence_file_uploader",
    )
    analyze_button = st.button(
        label="Analyze Document",
        key="analyze_button",
    )

    if analyze_button:
        if file_uploader is None:
            st.warning("Please upload a file first")
        else:
            with st.spinner("Analyzing..."):
                bytes_data = file_uploader.getvalue()
                response = asyncio.run(
                    http_post_file(
                        url=urljoin(base=backend_url, url="/azure_ai_document_intelligence/analyze_document"),
                        data_bytes_io=BytesIO(bytes_data),
                    )
                )
                st.write(response)


if __name__ == "__main__":
    main(
        backend_url=getenv("BACKEND_URL"),
        log_level=logging.DEBUG,
    )
