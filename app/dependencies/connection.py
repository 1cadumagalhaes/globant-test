from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres import PostgresSessionManager

postgres_manager = PostgresSessionManager()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with postgres_manager.session() as session:
        yield session
