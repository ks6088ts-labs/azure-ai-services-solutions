from logging import getLogger

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from internals.azure_storage_queue import Client
from schemas import azure_storage_queue as azure_storage_queue_schemas

from settings.azure_storage_queue import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_storage_queue",
    tags=["azure_storage_queue"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/queues",
    response_model=azure_storage_queue_schemas.CreateQueueResponse,
    status_code=200,
)
async def create_queue(
    body: azure_storage_queue_schemas.CreateQueueRequest,
):
    try:
        client.create_queue(
            queue_name=body.queue_name,
        )
    except Exception as e:
        logger.error(f"Failed to create queue: {e}")
        raise
    return azure_storage_queue_schemas.CreateQueueResponse(
        queue_name=body.queue_name,
    )


@router.delete(
    "/queues/{queue_name}",
    response_model=azure_storage_queue_schemas.DeleteQueueResponse,
    status_code=200,
)
async def delete_queue(
    queue_name: str,
):
    try:
        client.delete_queue(
            queue_name=queue_name,
        )
    except Exception as e:
        logger.error(f"Failed to delete queue: {e}")
        raise
    return azure_storage_queue_schemas.DeleteQueueResponse(
        queue_name=queue_name,
    )


@router.post(
    "/messages",
    response_model=azure_storage_queue_schemas.SendMessageResponse,
    status_code=200,
)
async def send_message(
    body: azure_storage_queue_schemas.SendMessageRequest,
):
    try:
        sent_message = client.send_message(
            queue_name=body.queue_name,
            message=body.message,
        )
        logger.info(f"Sent message: {sent_message}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise
    return azure_storage_queue_schemas.SendMessageResponse()


@router.get(
    "/messages",
    status_code=200,
)
async def receive_messages(
    queue_name: str,
    max_messages: int = 1,
):
    try:
        messages = client.receive_messages(
            queue_name=queue_name,
            max_messages=max_messages,
        )
        logger.info(f"Received messages: {messages}")
        message_list = []
        for message in messages:
            message_list.append(
                {
                    "id": message.id,
                    "message": message.content,
                    "pop_receipt": message.pop_receipt,
                }
            )
    except Exception as e:
        logger.error(f"Failed to receive messages: {e}")
        raise
    return JSONResponse(
        content=message_list,
    )


@router.delete(
    "/messages",
    response_model=azure_storage_queue_schemas.DeleteMessageResponse,
    status_code=200,
)
async def delete_message(
    body: azure_storage_queue_schemas.DeleteMessageRequest,
):
    try:
        client.delete_message(
            queue_name=body.queue_name,
            message_id=body.message_id,
            pop_receipt=body.pop_receipt,
        )
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")
        raise
    return azure_storage_queue_schemas.DeleteMessageResponse()
