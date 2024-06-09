from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_ai_vision_endpoint: str = "https://<name>.cognitiveservices.azure.com"
    azure_ai_vision_api_key: str = "<api-key>"

    model_config = SettingsConfigDict(
        env_file="settings/azure_ai_vision.env",
        env_file_encoding="utf-8",
    )
