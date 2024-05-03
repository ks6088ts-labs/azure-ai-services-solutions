from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class ChatCompletionRequest(BaseModel):
    content: str
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    content: str
