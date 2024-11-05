from typing import AsyncIterator

from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import PostgresSessionManager


@asynccontextmanager
async def get_db() -> AsyncIterator[AsyncSession]:
    ps_manager = PostgresSessionManager()
    session = ps_manager.session()
    if session is None:
        raise Exception('DatabaseSessionManager is not initialized')
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
