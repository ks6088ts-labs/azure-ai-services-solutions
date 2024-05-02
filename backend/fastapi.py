from fastapi import FastAPI

from backend.routers import azure_openai as azure_openai_router

app = FastAPI(
    docs_url="/",
)

app.include_router(azure_openai_router.router)
