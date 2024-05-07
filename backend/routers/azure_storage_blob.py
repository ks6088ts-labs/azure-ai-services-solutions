from logging import getLogger

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse

from backend.internals.azure_storage_blob import Client
from backend.schemas import azure_storage_blob as azure_storage_schemas
from backend.settings.azure_storage_blob import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_storage_blob",
    tags=["azure_storage_blob"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/blobs/upload",
    response_model=azure_storage_schemas.BlobUploadResponse,
    status_code=200,
)
async def upload_blob(
    file: UploadFile,
    blob_name: str,
):
    try:
        content = await file.read()
        client.upload_blob_stream(
            blob_name=blob_name,
            stream=content,
        )
    except Exception as e:
        logger.error(f"Failed to upload blob: {e}")
        raise
    return azure_storage_schemas.BlobUploadResponse(
        blob_name=blob_name,
    )


@router.delete(
    "/blobs/delete",
    status_code=200,
)
async def delete_blob(
    blob_name: str,
):
    try:
        client.delete_blob(
            blob_name=blob_name,
        )
    except Exception as e:
        logger.error(f"Failed to delete blob: {e}")
        raise
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"blob_name": blob_name},
    )


@router.get(
    "/blobs",
    status_code=200,
)
async def list_blobs():
    try:
        blobs = client.list_blobs()
    except Exception as e:
        logger.error(f"Failed to upload blob: {e}")
        raise
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"blobs": blobs},
    )
