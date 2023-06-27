from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from source.database.tables.User import User
from source.database.tables.Alert import Alert


class Connector:
    def __init__(self, connector):
        self.connector: async_sessionmaker[AsyncSession] = connector

    async def add_in_user(self, telegram_id: int, username: str, city: str = None,
                          status: str = 'member'):
        async with self.connector() as connector:
            async with connector.begin():
                connector.add(
                    User(
                        telegram_id=telegram_id,
                        username=username,
                        city=city,
                        status=status
                    )
                )
                return await connector.commit()

    async def update_status(self, user: int, status: str = 'member'):
        async with self.connector() as connector:
            async with connector.begin():
                await connector.execute(
                    update(User).where(User.telegram_id == user).values(status=status)
                )
                return await connector.commit()

    async def all_users(self, user: int) -> bool:
        async with self.connector() as connector:
            async with connector.begin():
                user = await connector.execute(
                    select(User).where(User.telegram_id == user)
                )
                return bool(user.fetchone())

    async def all_users_list(self):
        async with self.connector() as connector:
            async with connector.begin():
                try:
                    user = await connector.execute(select(User.telegram_id))
                    user = [i[0] for i in user.fetchall()]
                    return user
                except Exception:
                    pass

    # async def get_cities(self):
    #     async with self.connector() as connector:
    #         async with connector.begin():
    #             cities = set()
    #             cities_bd = await connector.execute(select(User.city))
    #             print(cities_bd.fetchall())
    #             for city_tuple in cities_bd.fetchall():
    #                 try:
    #                     async for city in city_tuple[0].split(', '):
    #                         cities.add(city)
    #                     cities.remove('')
    #                 except AttributeError:
    #                     pass
    #                 except KeyError:
    #                     pass
    #             return cities

    async def cities_of_user(self, user: int):
        async with self.connector() as connector:
            async with connector.begin():
                try:
                    cities = await connector.execute(select(User.city).where(
                        User.telegram_id == user
                    ))
                    cities = cities.fetchone()[0].split('\n')
                    while True:
                        try:
                            cities.remove('')
                        except Exception:
                            break
                    return cities
                except Exception:
                    return

    async def get_status_alert(self, user: int):
        async with self.connector() as connector:
            async with connector.begin():
                user = await connector.execute(
                    select(Alert).where(Alert.telegram_id == user)
                )
                return bool(user.fetchone())

    async def alert_city(self, user: int):
        async with self.connector() as connector:
            async with connector.begin():
                city = await connector.execute(
                    select(Alert.city).filter_by(telegram_id=user)
                )
                return city.fetchone()[0]

    async def remove_city(self, city: str, user: int):
        async with self.connector() as connector:
            async with connector.begin():
                cities = await connector.execute(select(User.city).where(User.telegram_id == user))
                cities = cities.first()[0].replace(city + '\n', '')
                request = await connector.execute(select(User).where(User.telegram_id == user))
                request.mappings().fetchone().get('User').city = cities
                return await connector.commit()
