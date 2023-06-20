import sqlalchemy
from core.database.session import SqlAlchemyBase


class User(SqlAlchemyBase):

    def __int__(self, telegram_id: int, username: str, cities: str, status: bool):
        self.telegram_id = telegram_id
        self.username = username
        self.city = cities
        self.status = status

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'User'

    lines = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        autoincrement=True,
        unique=True,
        primary_key=True
    )
    telegram_id = sqlalchemy.Column(
        sqlalchemy.BIGINT,
        nullable=False,
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
    status = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )


# async def get_cities_list(user: int):
#     with create_session() as db:
#         try:
#             cities = db.query(User.city).where(User.id == user).first()[0].split(', ')
#             return cities
#         except Exception:
#             return

#
# async def update_status(user_id: int, status: str) -> None:
#     """
#     Функция обновления статуса пользователя в бд
#     :param user_id: telegram user id
#     :param status: status must be str
#     :return: None
#     """
#     with create_session() as db:
#         db.query(User).where(
#             User.telegram_id == user_id
#         ).update({User.status: status})
#         db.commit()
