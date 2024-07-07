import asyncio
import contextlib
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from settings import settings


class Engines(object):
    pg_engine: AsyncEngine | None
    pg_session_maker: async_sessionmaker[AsyncSession] | None

    def __init__(self) -> None:
        self.make_connect()

    def make_connect(self):
        self.pg_engine = create_async_engine(
            settings.PG.ADDRESS,
            pool_size=25,
            max_overflow=10,
            pool_pre_ping=True,
        )
        self.pg_session_maker = async_sessionmaker(self.pg_engine, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        assert self.pg_session_maker is not None

        session = self.pg_session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        assert self.pg_engine is not None
        await self.pg_engine.dispose()

        self.pg_engine = None
        self.pg_session_maker = None

    async def test_connect(self):
        async def check_pg_connection():
            async with self.pg_engine.connect() as conn:
                await conn.execute(text("SELECT version()"))

        await asyncio.gather(check_pg_connection())


engine = Engines()
