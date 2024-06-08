from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.routers import azure_ai_document_intelligence as azure_ai_document_intelligence_router
from backend.routers import azure_ai_speech as azure_ai_speech_router
from backend.routers import azure_ai_vision as azure_ai_vision_router
from backend.routers import azure_cosmos_db as azure_cosmos_db_router
from backend.routers import azure_event_grid as azure_event_grid_router
from backend.routers import azure_openai as azure_openai_router
from backend.routers import azure_storage_blob as azure_storage_blob_router
from backend.routers import azure_storage_queue as azure_storage_queue_router

app = FastAPI(
    docs_url="/",
)

for router in [
    azure_ai_document_intelligence_router.router,
    azure_ai_vision_router.router,
    azure_event_grid_router.router,
    azure_openai_router.router,
    azure_storage_blob_router.router,
    azure_storage_queue_router.router,
    azure_cosmos_db_router.router,
    azure_ai_speech_router.router,
]:
    app.include_router(router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Azure AI Services Solutions",
        version="0.0.1",
        description="This contains a collection of solutions that leverage Azure AI services.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://news.microsoft.com/wp-content/uploads/prod/2022/05/Microsoft-logo_rgb_c-gray-1024x459.png"
    }
    openapi_schema["openapi"] = "3.0.0"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_version = "3.0.0"  # to use Kiota, downgrade to 3.0.0 (ref. https://github.com/microsoft/kiota/issues/3914)
app.openapi = custom_openapi
