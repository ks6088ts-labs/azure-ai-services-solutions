from logging import getLogger

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult
from settings.azure_iot_hub import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def get_device_twin(self) -> dict:
        client = IoTHubDeviceClient.create_from_connection_string(self.settings.azure_iot_hub_device_connection_string)
        # FIXME: to make it faster, connection should be established once and reused
        await client.connect()
        twin = await client.get_twin()
        await client.shutdown()
        return twin

    def invoke_direct_method(
        self,
        method_name: str,
        payload: str,
        device_id: str,
    ) -> dict:
        registry_manager = IoTHubRegistryManager(self.settings.azure_iot_hub_connection_string)
        # Call the direct method.
        deviceMethod = CloudToDeviceMethod(
            method_name=method_name,
            payload=payload,
        )
        response: CloudToDeviceMethodResult = registry_manager.invoke_device_method(
            device_id=device_id,
            direct_method_request=deviceMethod,
        )
        return response.as_dict()
