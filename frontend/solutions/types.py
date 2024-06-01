from enum import Enum


class SolutionType(Enum):
    SANDBOX = "SANDBOX"
    CHAT = "CHAT"
    CHAT_LANGCHAIN = "CHAT_LANGCHAIN"
    TRANSCRIPTION = "TRANSCRIPTION"
    DOCUMENT_INTELLIGENCE = "DOCUMENT_INTELLIGENCE"
    AZURE_STORAGE = "AZURE_STORAGE"
    AZURE_AI_VISION = "AZURE_AI_VISION"
