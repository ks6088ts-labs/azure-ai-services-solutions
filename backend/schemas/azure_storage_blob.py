from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class BlobUploadResponse(BaseModel):
    blob_name: str
