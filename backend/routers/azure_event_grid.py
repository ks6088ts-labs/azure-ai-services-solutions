from logging import getLogger

from fastapi import APIRouter

from backend.internals.azure_event_grid import Client
from backend.settings.azure_event_grid import Settings

logger = getLogger(__name__)

client = Client(
    settings=Settings(),
)

router = APIRouter(
    prefix="/azure_event_grid",
    tags=["azure_event_grid"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/event_grid_event/",
    status_code=200,
)
async def send_event_grid_event(
    data={"team": "azure-sdk"},
    subject="Door1",
    event_type="Azure.Sdk.Demo",
    data_version="2.0",
):
    try:
        client.send_event_grid_event(
            subject=subject,
            data=data,
            event_type=event_type,
            data_version=data_version,
        )
    except Exception as e:
        logger.error(f"Failed to analyze image: {e}")
        raise
    return
