from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_cosmos_db_endpoint: str = "https://<your-cosmos-db-name>.documents.azure.com:443/"
    azure_cosmos_db_key: str = "<your-cosmos-db-key>"
    azure_cosmos_db_connection_string: str = "<your-cosmos-db-connection-string>"

    model_config = SettingsConfigDict(
        env_file="settings/azure_cosmos_db.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
