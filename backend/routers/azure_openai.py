from logging import getLogger

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.internals import azure_openai

logger = getLogger(__name__)

router = APIRouter(
    prefix="/azure_openai",
    tags=["azure_openai"],
    responses={404: {"description": "Not found"}},
)


@router.post("/chat_completion/")
async def create_chat_completion(
    content: str,
    stream: bool = False,
):
    try:
        chat_completion = azure_openai.create_chat_completion(
            content=content,
            stream=stream,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            status_code=500,
            content={"message": str(e)},
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "success",
            "chat_completion": chat_completion,
        },
    )
