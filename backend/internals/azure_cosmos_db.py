from logging import getLogger

from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy

from settings.azure_cosmos_db import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_client(self) -> CosmosClient:
        return CosmosClient.from_connection_string(
            conn_str=self.settings.azure_cosmos_db_connection_string,
        )

    def get_database(self, database_id: str) -> DatabaseProxy:
        return self.get_client().get_database_client(database_id)

    def get_container(
        self,
        database_id: str,
        container_id: str,
    ) -> ContainerProxy:
        return self.get_database(database_id=database_id).get_container_client(container=container_id)

    def create_database(
        self,
        database_id: str,
    ) -> str:
        try:
            self.get_client().create_database_if_not_exists(
                id=database_id,
            )
        except AzureError as e:
            logger.error(e)
        return database_id

    def create_container(
        self,
        database_id: str,
        container_id: str,
        partition_key_path="/id",
    ) -> str:
        try:
            self.get_database(database_id=database_id).create_container_if_not_exists(
                id=container_id,
                partition_key=PartitionKey(
                    path=partition_key_path,
                ),
            )
        except AzureError as e:
            logger.error(e)
        return container_id

    def create_item(
        self,
        container: ContainerProxy,
        item: dict,
    ) -> dict:
        return container.create_item(
            body=item,
        )

    def read_item(
        self,
        container: ContainerProxy,
        item_id: str,
    ) -> dict:
        return container.read_item(
            item=item_id,
            partition_key=item_id,
        )

    def query_items(
        self,
        container: ContainerProxy,
        query: str,
        parameters: list | None = None,
        enable_cross_partition_query: bool = True,
    ) -> list:
        return container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=enable_cross_partition_query,
        )
