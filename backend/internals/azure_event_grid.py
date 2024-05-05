from logging import getLogger

from azure.core.credentials import AzureKeyCredential
from azure.eventgrid import EventGridEvent, EventGridPublisherClient

from backend.settings.azure_event_grid import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_client_from_access_key(self) -> EventGridPublisherClient:
        return EventGridPublisherClient(
            endpoint=self.settings.azure_event_grid_topic_endpoint,
            credential=AzureKeyCredential(self.settings.azure_event_grid_access_key),
        )

    def send_event_grid_event(
        self,
        subject: str,
        event_type: str,
        data: dict,
        data_version: str,
    ) -> None:
        try:
            client = self.get_client_from_access_key()
            client.send(
                EventGridEvent(
                    subject=subject,
                    data=data,
                    event_type=event_type,
                    data_version=data_version,
                )
            )
            logger.info(f"Event sent: {event_type}")
        except Exception as e:
            logger.error(f"Failed to send event: {e}")
            raise e
