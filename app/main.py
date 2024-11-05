from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

from app.config import Settings
from app.dependencies.connection import get_db
from app.models.responses import Message


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
