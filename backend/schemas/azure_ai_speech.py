from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class CreateTranscriptionRequest(BaseModel):
    content_url: str = "https://<blob_account_name>.blob.core.windows.net/<blob_container_name>/<blob_name>"
    locale: str = "ja-JP"


class CreateTranscriptionResponse(BaseModel):
    transcription_id: str
