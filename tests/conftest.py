import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer

from app import models  # noqa: F401
from app.config import Settings
from app.dependencies.connection import get_db
from app.main import app as fastapi_app
from tests.test_data import (
    create_test_departments,
    create_test_employees,
    create_test_jobs,
)

settings = Settings()


@pytest.fixture(scope='module')
def event_loop():
    """Create a single event loop for the session scope."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='module')
def postgres_container():
    """Set up PostgresContainer without async context."""
    container = PostgresContainer(
        'postgres:16',
        username='test_user',
        password='test_pass',
        dbname='test_db',
    )
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope='module')
async def async_engine(postgres_container, event_loop):
    db_url = postgres_container.get_connection_url()
    async_db_url = f'postgresql+asyncpg://{db_url.split("://", 1)[1]}'

    _engine = create_async_engine(
        async_db_url,
        echo=settings.verbose_db,
        future=True,
    )
    asyncio.set_event_loop(event_loop)

    yield _engine
    await _engine.dispose()


@pytest.fixture(scope='module')
async def async_session(async_engine: AsyncSession, event_loop):
    """Create a new async session for each test."""
    async_session_maker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=True,
    )
    asyncio.set_event_loop(event_loop)

    async with async_session_maker() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        yield session
        await session.rollback()
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def async_client(async_session: AsyncSession) -> AsyncClient:  # type: ignore
    """Create an async client for testing FastAPI endpoints."""

    async def get_postgres_session_override():
        yield async_session

    fastapi_app.dependency_overrides[get_db] = get_postgres_session_override
    client = AsyncClient(app=fastapi_app, base_url='http://test')
    yield client
    await client.aclose()
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope='module')
async def populated_async_session(async_session):
    """Fixture to provide a session with pre-populated test data."""
    departments = create_test_departments()
    jobs = create_test_jobs()
    employees = create_test_employees()

    async_session.add_all(departments)
    async_session.add_all(jobs)
    async_session.add_all(employees)
    await async_session.commit()

    yield async_session

    await async_session.rollback()
