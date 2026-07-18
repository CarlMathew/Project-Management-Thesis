from contextlib import asynccontextmanager
from collections.abc import AsyncIterator


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

import logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app:FastAPI) -> AsyncIterator[None]:
    logger.info(f"Starting {settings.app_name}")
    yield
    logger.info(f"Stopping {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url = "/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
def get_root() -> dict[str, str]:
    return {
        "message": settings.app_name,
        "documentation": "/docs"
    }