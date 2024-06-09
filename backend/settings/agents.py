from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    agents_azure_openai_endpoint: str = "https://<aoai-name>.openai.azure.com"
    agents_azure_openai_api_key: str = "<aoai-api-key>"
    agents_azure_openai_api_version: str = "2024-05-01-preview"
    agents_azure_openai_gpt_model: str = "gpt-4o"

    model_config = SettingsConfigDict(
        env_file="settings/agents.env",
        env_file_encoding="utf-8",
    )
