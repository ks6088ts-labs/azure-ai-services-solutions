import logging
from os import getenv, makedirs

import streamlit as st
from audiorecorder import audiorecorder
from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types.audio import Transcription

logger = logging.getLogger(__name__)
load_dotenv()


# TODO: call backend API instead of using Azure OpenAI
def get_transcription(file_path: str) -> Transcription:
    client = AzureOpenAI(
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
    )

    return client.audio.transcriptions.create(
        file=open(file=file_path, mode="rb"),
        model=getenv("AZURE_OPENAI_MODEL_WHISPER"),
    )


def main(
    backend_url: str,
    log_level: int,
):
    # Logger
    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.write("Transcription")

    # create directory if not exists
    # TODO: remove hard coded path
    makedirs("artifacts", exist_ok=True)

    # Audio settings
    audio_file_path = "artifacts/audio.wav"

    audio = audiorecorder(
        start_prompt="",
        stop_prompt="",
        pause_prompt="",
        show_visualizer=True,
        key=None,
    )

    if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.export().read())
        # To save audio to a file, use pydub export method:
        audio.export(audio_file_path, format="wav")
        # To get audio properties, use pydub AudioSegment properties:
        st.write(
            f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds"  # noqa
        )
        with st.spinner("Transcribing..."):
            # Get transcription
            transcription = get_transcription(audio_file_path)
            st.write(f"Transcription: {transcription.text}")


if __name__ == "__main__":
    main(
        backend_url=getenv("BACKEND_URL"),
        log_level=logging.DEBUG,
    )
