import asyncio
import logging
from io import BytesIO
from urllib.parse import urljoin

import streamlit as st

from frontend.solutions.utilities import http_post_file

logger = logging.getLogger(__name__)


def start(
    backend_url: str,
    log_level: int,
):
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.header("Azure Storage")

    file_uploader = st.file_uploader(
        label="Choose a file",
        key="file_uploader",
    )
    blob_name = st.text_input(
        label="Blob Name",
        key="blob_name",
    )
    upload_button = st.button(
        label="Upload File",
        key="upload_button",
    )

    if upload_button:
        if file_uploader is None:
            st.warning("Please upload a file first")
        else:
            with st.spinner("Uploading..."):
                bytes_data = file_uploader.getvalue()
                response = asyncio.run(
                    http_post_file(
                        url=urljoin(base=backend_url, url=f"/azure_storage/blobs/upload/?blob_name={blob_name}"),
                        data_bytes_io=BytesIO(bytes_data),
                    )
                )
                st.write(response)
