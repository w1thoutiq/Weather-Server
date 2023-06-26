import sqlalchemy
from source.database.session import SqlAlchemyBase


class Alert(SqlAlchemyBase):

    def __repr__(self):
        return f'{self.telegram_id} {self.username} {self.city} {self.status}'

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

    row = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True,
                            unique=True, primary_key=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False,
                                    unique=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    timezone = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False)
