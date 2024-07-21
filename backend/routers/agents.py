from logging import getLogger

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from internals.agent_search import Client
from schemas import agents as agents_schemas
from settings.agents import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/search",
    status_code=200,
)
async def search(request: agents_schemas.SearchRequest):
    response = client.invoke(
        system_prompt=request.system_prompt,
        user_prompt=request.prompt,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(response),
    )
