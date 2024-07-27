from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    agents_azure_openai_endpoint: str = "https://<aoai-name>.openai.azure.com"
    agents_azure_openai_api_key: str = "<aoai-api-key>"
    agents_azure_openai_api_version: str = "2024-06-01"
    agents_azure_openai_model_chat: str = "gpt-4o"

    agents_langchain_tracing_v2: str = "false"
    agents_langchain_api_key: str = "<langchain-api-key>"

    model_config = SettingsConfigDict(
        env_file="agents.env",
        env_file_encoding="utf-8",
    )
