from environs import Env
from dataclasses import dataclass


@dataclass
class Environs:
    db_name: str
    db_pass: str
    db_username: str


@dataclass
class Bot:
    token: str
    admin_id: int


@dataclass
class Settings:
    bot: Bot
    env: Environs


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bot=Bot(
            token=env.str('TOKEN_BOT'),
            admin_id=env.int('ADMIN_ID')
        ),
        env=Environs(
            db_name=env.str('NAME'),
            db_pass=env.str('DB_PASS'),
            db_username=env.str('DB_USERNAME')
        )
    )


settings = get_settings('source/.env')
