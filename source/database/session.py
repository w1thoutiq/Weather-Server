# import logging
import logging
from typing import Union

from sqlalchemy import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, \
    create_async_engine, async_sessionmaker, AsyncEngine

from source.settings import settings

SqlAlchemyBase = declarative_base()


postgres_url = URL.create(
    'postgresql+asyncpg',
    username=settings.env.db_username,
    password=settings.env.db_pass,
    host='localhost',
    port=5432,
    database=settings.env.db_name
)


def get_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return create_async_engine(url=url, echo=False)


async def create_all_scheme(engine: AsyncEngine):
    async with engine.begin() as connector:
        return await connector.run_sync(SqlAlchemyBase.metadata.create_all)


async def create_session(
        engine: AsyncEngine = create_async_engine(
            url=postgres_url,
            echo=False
        )
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False,
                              class_=AsyncSession)


async def connect_database() -> None:
    engine = get_async_engine(postgres_url)
    await create_all_scheme(engine)
    logging.info(f"Подключено к базе данных {settings.env.db_name}\n{postgres_url}")

