from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_iot_hub_device_connection_string: str = (
        "HostName=<iot-hub-name>.azure-devices.net;DeviceId=<device-name>;SharedAccessKey=<shared-access-key>"
    )
    azure_iot_hub_connection_string: str = (
        "HostName=<iot-hub-name>.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=<shared-access-key>"
    )

    model_config = SettingsConfigDict(
        env_file="azure_iot_hub.env",
        env_file_encoding="utf-8",
    )
