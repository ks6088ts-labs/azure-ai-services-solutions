from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    endpoint: str = "https://<aoai-name>.openai.azure.com/"
    api_key: str = "<aoai-api-key>"
    api_version: str = "2024-02-01"
    embedding_model: str = "text-embedding-ada-002"
    gpt_model: str = "gpt-35-turbo"

    model_config = SettingsConfigDict(
        env_file="azure_openai.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
