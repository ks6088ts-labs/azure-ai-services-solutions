from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_event_grid_access_key: str = "<access-key>"
    azure_event_grid_topic_endpoint: str = "<name>.<region>.eventgrid.azure.net"

    model_config = SettingsConfigDict(
        env_file="settings/azure_event_grid.env",
        env_file_encoding="utf-8",
    )
