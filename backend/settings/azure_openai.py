from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_endpoint: str = "https://<aoai-name>.openai.azure.com/"
    azure_openai_api_key: str = "<aoai-api-key>"
    azure_openai_api_version: str = "2024-02-01"
    azure_openai_embedding_model: str = "text-embedding-ada-002"
    azure_openai_gpt_model: str = "gpt-35-turbo"
    azure_openai_gpt4_model: str = "gpt-4-turbo-2024-04-09"

    model_config = SettingsConfigDict(
        env_file="azure_openai.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
