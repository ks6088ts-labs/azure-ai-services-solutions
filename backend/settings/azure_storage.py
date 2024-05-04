from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_storage_account_name: str = "<account-name>"
    azure_storage_sas_token: str = "<sas-token>"
    azure_storage_blob_container_name: str = "<blob-container-name>"

    model_config = SettingsConfigDict(
        env_file="azure_storage.env",
        env_file_encoding="utf-8",
    )
