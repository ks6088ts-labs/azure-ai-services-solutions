from logging import getLogger

from azure.core.paging import ItemPaged
from azure.storage.queue import QueueMessage, QueueServiceClient
from settings.azure_storage_queue import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings):
        self.client = QueueServiceClient.from_connection_string(settings.azure_storage_queue_connection_string)

    def create_queue(
        self,
        queue_name: str,
    ):
        queue_client = self.client.get_queue_client(queue_name)
        queue_client.create_queue()
        logger.info(f"Created queue {queue_name}")

    def delete_queue(
        self,
        queue_name: str,
    ):
        queue_client = self.client.get_queue_client(queue_name)
        queue_client.delete_queue()
        logger.info(f"Deleted queue {queue_name}")

    def send_message(
        self,
        queue_name: str,
        message: str,
    ) -> QueueMessage:
        queue_client = self.client.get_queue_client(queue_name)
        sent_message = queue_client.send_message(
            content=message,
        )
        logger.info(f"Sent message to queue {queue_name}")
        return sent_message

    def get_queue_properties(
        self,
        queue_name: str,
    ):
        queue_client = self.client.get_queue_client(queue_name)
        properties = queue_client.get_queue_properties()
        logger.info(f"Got properties of queue {queue_name}")
        return properties

    def receive_messages(
        self,
        queue_name: str,
        max_messages: int = 1,
    ) -> ItemPaged[QueueMessage]:
        queue_client = self.client.get_queue_client(queue_name)
        messages = queue_client.receive_messages(
            max_messages=max_messages,
        )
        logger.info(f"Received messages from queue {queue_name}")
        return messages

    def delete_message(
        self,
        queue_name: str,
        message_id: str,
        pop_receipt: str,
    ):
        queue_client = self.client.get_queue_client(queue_name)
        queue_client.delete_message(
            message=message_id,
            pop_receipt=pop_receipt,
        )
        logger.info(f"Deleted message from queue {queue_name}")
