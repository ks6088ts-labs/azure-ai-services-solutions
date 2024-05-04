from logging import getLogger

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse

from backend.internals import azure_storage
from backend.schemas import azure_storage as azure_storage_schemas
from backend.settings.azure_storage import Settings as AzureStorageSettings

logger = getLogger(__name__)
blob_storage_client = azure_storage.BlobStorageClient(
    settings=AzureStorageSettings(),
)

router = APIRouter(
    prefix="/azure_storage",
    tags=["azure_storage"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/blobs/upload/",
    response_model=azure_storage_schemas.BlobUploadResponse,
    status_code=200,
)
async def upload_blob(
    file: UploadFile,
    blob_name: str,
):
    try:
        content = await file.read()
        blob_storage_client.upload_blob_stream(
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
    "/blobs/delete/",
    status_code=200,
)
async def delete_blob(
    blob_name: str,
):
    try:
        blob_storage_client.delete_blob(
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
    "/blobs/",
    status_code=200,
)
async def list_blobs():
    try:
        blobs = blob_storage_client.list_blobs()
    except Exception as e:
        logger.error(f"Failed to upload blob: {e}")
        raise
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"blobs": blobs},
    )
