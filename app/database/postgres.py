from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,  # type: ignore
    create_async_engine,
)

from app.config import Settings


class PostgresSessionManager:
    """ """

    def __init__(self):
        settings = Settings()
        self._connection_url = str(settings.postgres_uri)
        self._verbose_db = settings.verbose_db
        self.pool_size = settings.postgres_pool_size
        self.engine: AsyncEngine | None = None
        self.connection: AsyncConnection | None = None
        self.session_maker = None
        self.session = None
        self.init_db()
        self.instrument_asyncpg()

    def init_db(self):
        async_engine = create_async_engine(
            url=self._connection_url,
            echo=self._verbose_db,
            echo_pool=self._verbose_db,
            pool_size=self.pool_size,
            max_overflow=1,
            pool_timeout=30,
            pool_recycle=1800,
            connect_args={
                'server_settings': {'application_name': 'retigazer'},
            },
            pool_pre_ping=True,
        )
        self.engine = async_engine
        self.session_maker = async_sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )

        self.session = async_scoped_session(
            self.session_maker, scopefunc=current_task
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
        if self.engine:
            await self.engine.dispose()
