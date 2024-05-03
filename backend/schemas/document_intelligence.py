from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class AnalyzeDocumentRequest(BaseModel):
    content: bytes


class AnalyzeDocumentResponse(BaseModel):
    content: str
