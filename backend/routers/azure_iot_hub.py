from logging import getLogger

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.internals.azure_iot_hub import Client
from backend.settings.azure_iot_hub import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_iot_hub",
    tags=["azure_iot_hub"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/device_twin",
    status_code=200,
)
async def get_device_twin():
    device_twin = await client.get_device_twin()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=device_twin,
    )


@router.post(
    "/event_grid_event",
    status_code=200,
)
async def invoke_direct_method(
    device_id="device001",
    method_name="method1",
    payload={"hello": "world"},
):
    response = client.invoke_direct_method(
        device_id=device_id,
        method_name=method_name,
        payload=payload,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response,
    )
