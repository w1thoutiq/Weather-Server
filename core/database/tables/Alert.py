import sqlalchemy
from core.database.session import SqlAlchemyBase


class Alert(SqlAlchemyBase):

    def __int__(
            self,
            telegram_id: int,
            username: str,
            city: str,
            timezone: int
    ):
        self.id = telegram_id
        self.username = username
        self.city = city
        self.timezone = timezone

    __table_args__ = {'extend_existing': True}
    __tablename__ = 'Alert'

    lines = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True,
                              unique=True, primary_key=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timezone = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False)
