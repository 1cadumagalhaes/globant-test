import logging
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

from app.config import Settings
from app.dependencies.connection import get_db
from app.models.responses import Message
from app.routes.upload import router as upload_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
app = FastAPI(
    title=settings.api_name,
    version=settings.api_version,
    lifespan=lifespan,
    debug=settings.environment != 'production',
    dependencies=[Depends(get_db)],
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!!!'}


app.include_router(upload_router)
