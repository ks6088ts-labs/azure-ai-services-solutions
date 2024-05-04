from logging import getLogger

from azure.storage.blob import BlobServiceClient

from backend.settings import azure_storage as azure_storage_settings

logger = getLogger(__name__)


class BlobStorageClient:
    def __init__(self, settings: azure_storage_settings.Settings):
        self.settings = settings

    def get_blob_service_client(self) -> BlobServiceClient:
        return BlobServiceClient(
            account_url=f"https://{self.settings.azure_storage_account_name}.blob.core.windows.net",
            credential=self.settings.azure_storage_sas_token,
        )

    def upload_blob_stream(
        self,
        container_name: str,
        blob_name: str,
        stream: bytes,
    ):
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name,
        )
        blob_client.upload_blob(stream, overwrite=True)
        logger.info(f"Uploaded blob {blob_name} to container {container_name}")

    def download_blob_stream(
        self,
        container_name: str,
        blob_name: str,
    ) -> bytes:
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name,
        )
        stream = blob_client.download_blob().readall()
        logger.info(f"Downloaded blob {blob_name} from container {container_name}")
        return stream

    def delete_blob(
        self,
        container_name: str,
        blob_name: str,
    ):
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name,
        )
        blob_client.delete_blob()
        logger.info(f"Deleted blob {blob_name} from container {container_name}")

    def list_blobs(
        self,
        container_name: str,
    ) -> list:
        blob_service_client = self.get_blob_service_client()
        container_client = blob_service_client.get_container_client(container_name)
        return container_client.list_blobs()
