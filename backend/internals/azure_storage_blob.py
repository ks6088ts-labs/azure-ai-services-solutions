from logging import getLogger

from azure.storage.blob import BlobServiceClient

from settings.azure_storage_blob import Settings

logger = getLogger(__name__)


class Client:
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_blob_service_client(self) -> BlobServiceClient:
        return BlobServiceClient(
            account_url=f"https://{self.settings.azure_storage_blob_account_name}.blob.core.windows.net",
            credential=self.settings.azure_storage_blob_sas_token,
        )

    def upload_blob_stream(
        self,
        blob_name: str,
        stream: bytes,
    ):
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=self.settings.azure_storage_blob_container_name,
            blob=blob_name,
        )
        blob_client.upload_blob(stream, overwrite=True)
        logger.info(f"Uploaded blob {blob_name} to container {self.settings.azure_storage_blob_container_name}")

    def download_blob_stream(
        self,
        blob_name: str,
    ) -> bytes:
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=self.settings.azure_storage_blob_container_name,
            blob=blob_name,
        )
        stream = blob_client.download_blob().readall()
        logger.info(f"Downloaded blob {blob_name} from container {self.settings.azure_storage_blob_container_name}")
        return stream

    def delete_blob(
        self,
        blob_name: str,
    ):
        blob_service_client = self.get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(
            container=self.settings.azure_storage_blob_container_name,
            blob=blob_name,
        )
        blob_client.delete_blob()
        logger.info(f"Deleted blob {blob_name} from container {self.settings.azure_storage_blob_container_name}")

    def list_blobs(
        self,
    ) -> list:
        blob_service_client = self.get_blob_service_client()
        container_client = blob_service_client.get_container_client(self.settings.azure_storage_blob_container_name)
        logger.info(f"Listed blobs in container {self.settings.azure_storage_blob_container_name}")
        return [blob.name for blob in container_client.list_blobs()]
