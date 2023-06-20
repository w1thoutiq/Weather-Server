import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return
    if not db_file or not db_file.strip():
        raise ValueError("Необходимо указать файл базы данных.")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)
    logging.info(f"Подключение к базе данных {db_file}")


def create_session() -> Session:
    global __factory
    return __factory()
