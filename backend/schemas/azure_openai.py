from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class ChatCompletionRequest(BaseModel):
    content: str


class ChatCompletionResponse(BaseModel):
    content: str


class ChatCompletionStreamRequest(BaseModel):
    content: str


class ChatCompletionWithVisionResponse(BaseModel):
    content: str
