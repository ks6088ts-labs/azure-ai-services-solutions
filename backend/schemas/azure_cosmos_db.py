from logging import getLogger

from pydantic import BaseModel

logger = getLogger(__name__)


class CreateDatabaseRequest(BaseModel):
    database_id: str


class CreateDatabaseResponse(BaseModel):
    database_id: str


class CreateContainerRequest(BaseModel):
    container_id: str
    database_id: str


class CreateContainerResponse(BaseModel):
    container_id: str


class CreateItemRequest(BaseModel):
    container_id: str
    database_id: str
    item: dict


class CreateItemResponse(BaseModel):
    container_id: str
    database_id: str
    item: dict


class ReadItemResponse(BaseModel):
    item: dict
