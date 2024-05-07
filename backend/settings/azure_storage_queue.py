from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_storage_queue_connection_string: str = "<connection-string>"

    model_config = SettingsConfigDict(
        env_file="azure_storage_queue.env",
        env_file_encoding="utf-8",
    )
