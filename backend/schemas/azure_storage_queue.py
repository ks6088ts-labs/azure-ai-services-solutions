from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class CreateQueueRequest(BaseModel):
    queue_name: str


class CreateQueueResponse(BaseModel):
    queue_name: str


class DeleteQueueResponse(BaseModel):
    queue_name: str


class SendMessageRequest(BaseModel):
    queue_name: str
    message: str


class SendMessageResponse(BaseModel):
    pass


class DeleteMessageRequest(BaseModel):
    queue_name: str
    message_id: str
    pop_receipt: str


class DeleteMessageResponse(BaseModel):
    pass
