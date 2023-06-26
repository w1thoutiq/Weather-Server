# import logging
from typing import Union

from sqlalchemy import URL
# from sqlalchemy.orm import session maker
# from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, \
    create_async_engine, async_sessionmaker, AsyncEngine

SqlAlchemyBase = declarative_base()


# class SqlAlchemyBase(AsyncAttrs, DeclarativeBase):
#     pass


# url_global = ''
# __factory = None
# session = None


# async def global_init(db_file):
#     global __factory
#     if __factory:
#         return
#     if not db_file or not db_file.strip():
#         raise ValueError("Необходимо указать файл базы данных.")
#     conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
#     engine = create_engine(conn_str, echo=False)
#     __factory = sessionmaker(bind=engine)
#     SqlAlchemyBase.metadata.create_all(engine)
#     logging.info(f"Подключение к базе данных {db_file}")
#
#
# def create_session() -> Session:
#     global __factory
#     return __factory()

def get_async_engine(url: Union[URL, str]):
    return create_async_engine(url=url, echo=False)


async def create_all_scheme(engine: AsyncEngine):
    async with engine.begin() as connector:
        await connector.run_sync(SqlAlchemyBase.metadata.create_all)


async def create_session(
        engine: AsyncEngine = create_async_engine(
            url='postgresql+asyncpg://postgres:***@localhost:5432/TelegramDataBase',
            echo=False
        )
):
    return async_sessionmaker(engine, expire_on_commit=False,
                              class_=AsyncSession)



# def schemas(session: AsyncSession):
#     with session.begin():
#         session.run_sync(SqlAlchemyBase.metadata.create_all())


# def create_session(engine: AsyncEngine):
#     return sessionmaker(engine, class_=AsyncSession)


# async def create_session(engine: AsyncEngine):
#     return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
