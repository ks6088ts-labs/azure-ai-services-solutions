import uvicorn


def start(
    host: str,
    port: int,
    log_level: int,
    reload: bool,
):
    uvicorn.run(
        "backend.fastapi:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )
