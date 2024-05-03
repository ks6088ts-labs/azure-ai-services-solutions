from fastapi import FastAPI

from backend.routers import azure_openai as azure_openai_router
from backend.routers import document_intelligence as document_intelligence_router

app = FastAPI(
    docs_url="/",
)

app.include_router(azure_openai_router.router)
app.include_router(document_intelligence_router.router)
