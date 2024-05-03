import logging
import time
from os import getenv

import azure.cognitiveservices.speech as speechsdk
import streamlit as st
from azure.cognitiveservices.speech.speech import SpeechRecognitionEventArgs
from dotenv import load_dotenv

load_dotenv("azure_ai_speech.env")
logger = logging.getLogger(__name__)
done = False


def transcript(
    subscription: str,
    region: str,
    speech_recognition_language: str,
):
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speechsdk.SpeechConfig(
            subscription=subscription,
            region=region,
            speech_recognition_language=speech_recognition_language,
        ),
        audio_config=speechsdk.audio.AudioConfig(
            use_default_microphone=True,
        ),
    )

    def stop_cb(evt: SpeechRecognitionEventArgs):
        logger.debug(f"CLOSING on {evt}")
        speech_recognizer.stop_continuous_recognition()

    def recognized_cb(evt: SpeechRecognitionEventArgs):
        logger.debug(f"RECOGNIZED: {evt}")
        new_text = evt.result.text.strip()
        logger.info(new_text)
        # FIXME: App does not show the transcription

    speech_recognizer.recognizing.connect(lambda evt: logger.debug(f"RECOGNIZING: {evt}"))
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: logger.debug(f"SESSION STARTED: {evt}"))
    speech_recognizer.session_stopped.connect(lambda evt: logger.debug(f"SESSION STOPPED {evt}"))
    speech_recognizer.canceled.connect(lambda evt: logger.debug(f"CANCELED {evt}"))
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    global done

    if st.button("Stop transcription", key="stop_transcription"):
        # FIXME: App does not stop transcription
        logger.info("Stop transcription")
        speech_recognizer.stop_continuous_recognition()
        done = True

    while done is False:
        time.sleep(0.5)


def start(
    backend_url: str,
    log_level: int,
):
    global done

    logger.setLevel(log_level)
    logger.debug(f"set log level to {log_level}")

    st.write("Transcription")

    if st.button("Start transcription", key="start_transcription"):
        logger.info("Start transcription...")
        done = False
        try:
            with st.spinner("Transcribing..."):
                transcript(
                    subscription=getenv("AZURE_AI_SPEECH_SUBSCRIPTION_KEY"),
                    region=getenv("AZURE_AI_SPEECH_REGION"),
                    speech_recognition_language=getenv("AZURE_AI_SPEECH_RECOGNITION_LANGUAGE"),
                )
        except Exception as e:
            st.write(f"Error: {e}")
            logger.error(f"Error: {e}")
