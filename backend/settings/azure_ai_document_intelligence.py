from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_ai_document_intelligence_endpoint: str = (
        "https://<your-document-intelligence-name>.cognitiveservices.azure.com"
    )
    azure_ai_document_intelligence_api_key: str = "<your-document-intelligence-api-key>"

    model_config = SettingsConfigDict(
        env_file="azure_ai_document_intelligence.env",
        env_file_encoding="utf-8",
    )
