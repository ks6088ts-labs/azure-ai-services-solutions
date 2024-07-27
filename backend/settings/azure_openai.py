from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_endpoint: str = "https://<aoai-name>.openai.azure.com"
    azure_openai_api_key: str = "<aoai-api-key>"
    azure_openai_api_version: str = "2024-06-01"
    azure_openai_embedding_model: str = "text-embedding-3-large"
    azure_openai_gpt_model: str = "gpt-4o"

    model_config = SettingsConfigDict(
        env_file="azure_openai.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
