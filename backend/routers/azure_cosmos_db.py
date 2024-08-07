from logging import getLogger

from fastapi import APIRouter
from internals.azure_cosmos_db import Client
from schemas import azure_cosmos_db as azure_cosmos_db_schemas
from settings.azure_cosmos_db import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_cosmos_db",
    tags=["azure_cosmos_db"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/database",
    response_model=azure_cosmos_db_schemas.CreateDatabaseResponse,
    status_code=200,
)
async def create_database(body: azure_cosmos_db_schemas.CreateDatabaseRequest):
    database_id = client.create_database(
        database_id=body.database_id,
    )
    return azure_cosmos_db_schemas.CreateDatabaseResponse(
        database_id=database_id,
    )


@router.post(
    "/container",
    response_model=azure_cosmos_db_schemas.CreateContainerResponse,
    status_code=200,
)
async def create_container(body: azure_cosmos_db_schemas.CreateContainerRequest):
    container_id = client.create_container(
        container_id=body.container_id,
        database_id=body.database_id,
    )
    return azure_cosmos_db_schemas.CreateContainerResponse(
        container_id=container_id,
    )


@router.post(
    "/item",
    response_model=azure_cosmos_db_schemas.CreateItemResponse,
    status_code=200,
)
async def create_item(body: azure_cosmos_db_schemas.CreateItemRequest):
    container = client.get_container(
        container_id=body.container_id,
        database_id=body.database_id,
    )
    created_item = client.create_item(
        container=container,
        item=body.item,
    )
    return azure_cosmos_db_schemas.CreateItemResponse(
        container_id=body.container_id,
        database_id=body.database_id,
        item=created_item,
    )


@router.get(
    "/{database_id}/{container_id}/{item_id}",
    response_model=azure_cosmos_db_schemas.ReadItemResponse,
    status_code=200,
)
async def read_item(
    database_id: str,
    container_id: str,
    item_id: str,
):
    container = client.get_container(
        database_id=database_id,
        container_id=container_id,
    )
    read_item = client.read_item(
        container=container,
        item_id=item_id,
    )
    return azure_cosmos_db_schemas.ReadItemResponse(
        item=read_item,
    )
