from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.routers import azure_ai_vision as azure_ai_vision_router
from backend.routers import azure_openai as azure_openai_router
from backend.routers import azure_storage as azure_storage_router
from backend.routers import document_intelligence as document_intelligence_router

app = FastAPI(
    docs_url="/",
)

app.include_router(azure_openai_router.router)
app.include_router(document_intelligence_router.router)
app.include_router(azure_storage_router.router)
app.include_router(azure_ai_vision_router.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Azure AI Services Solutions",
        version="0.0.1",
        description="This contains a collection of solutions that leverage Azure AI services.",
        routes=app.routes,
        servers=[
            {
                "url": "http://localhost:8000",
            }
        ],
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://news.microsoft.com/wp-content/uploads/prod/2022/05/Microsoft-logo_rgb_c-gray-1024x459.png"
    }
    openapi_schema["openapi"] = "3.0.0"
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_version = "3.0.0"  # to use Kiota, downgrade to 3.0.0 (ref. https://github.com/microsoft/kiota/issues/3914)
app.openapi = custom_openapi
