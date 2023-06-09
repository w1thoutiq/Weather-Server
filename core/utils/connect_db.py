import sqlalchemy
from core.utils.session_db import SqlAlchemyBase, create_session


class User(SqlAlchemyBase):

    def __int__(self, id: int, username: str, cities: str, status: bool):
        self.id = id
        self.username = username
        self.city = cities
        self.active = status

    __tablename__ = 'base'

    username = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    id = sqlalchemy.Column(
        sqlalchemy.BIGINT,
        nullable=False,
        primary_key=True,
        unique=True
    )
    city = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    active = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False
    )


async def update_status(user_id: int, status: bool = False) -> None:
    """
    Функция обновления статуса пользователя в бд
    :param user_id: telegram user id
    :param status: status must be str
    :return: None
    """
    with create_session() as db:
        db.query(User).where(
            User.id == user_id
        ).update({User.active: status})
        db.commit()


class Alert(SqlAlchemyBase):

    def __int__(self, id: int, username: str, city: str, timezone: int):
        self.id = id
        self.username = username
        self.city = city
        self.timezone = timezone

    __tablename__ = 'alerts_base'

    id = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        primary_key=True,
        unique=True
    )
    username = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    city = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    timezone = sqlalchemy.Column(
        sqlalchemy.BIGINT,
        nullable=False
    )


class AlertGraph(SqlAlchemyBase):
    __tablename__ = 'temperature_graph'

    city = sqlalchemy.Column(
        sqlalchemy.TEXT,
        nullable=False,
        unique=True,
        primary_key=True
    )
    am12 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am1 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am2 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am3 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am4 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am5 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am6 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am7 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am8 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am9 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am10 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    am11 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm12 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm1 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm2 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm3 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm4 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm5 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm6 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm7 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm8 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm9 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm10 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)
    pm11 = sqlalchemy.Column(sqlalchemy.FLOAT, nullable=True)


def __repr__(self):
    return '<User %r>' % self.username
