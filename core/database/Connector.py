from core.database.__all__ import User, Alert
from core.database.session import create_session


class Connector:
    def __init__(self):
        self.connector = create_session

    async def add_in_user(self, telegram_id: int, username: str, city: str = None,
                          status: str = 'member'):
        with self.connector() as connector:
            connector.add(
                User(telegram_id=telegram_id, username=username, city=city,
                     status=status)
            )
            return connector.commit()

    async def update_status(self, user: int, status: str = 'member'):
        with self.connector() as connector:
            connector.query(User).where(User.telegram_id == user).update(
                {User.status: status}
            )
            return connector.commit()

    async def all_users(self):
        with self.connector() as connector:
            return [
                user[0] for user in connector.query(User.telegram_id).all()
            ]

    async def get_cities(self):
        with self.connector() as connector:
            cities = set()
            for city_tuple in connector.query(User.city).all():
                try:
                    for city in city_tuple[0].split(', '):
                        cities.add(city)
                    cities.remove('')
                except AttributeError:
                    pass
                except KeyError:
                    pass

    async def cities_of_user(self, user: int):
        with self.connector() as connector:
            try:
                cities = connector.query(User.city).where(
                    User.telegram_id == user
                ).first()[0].split(', ')
                return cities
            except Exception:
                return

    async def get_status_alert(self, user: int):
        with self.connector() as connector:
            return bool(connector.query(Alert).where(Alert.telegram_id == user).first())

    async def alert_city(self, user: int):
        with self.connector() as connector:
            return connector.query(Alert.city).filter_by(telegram_id=user).first()[0]

    async def remove_city(self, city: str, user: int):
        with self.connector() as connector:
            cities = connector.query(User.city).where(User.telegram_id == user).first()[0].replace(city + ', ', '')
            connector.query(User).where(User.telegram_id == user).update({User.city: cities})
            connector.commit()
