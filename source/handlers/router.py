from datetime import timedelta, datetime as dt

from aiogram import Dispatcher
# from aiogram import Router, F
# from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionMiddleware

from source.middlewares.filters import IsNotPrivate
# from source.middlewares.filters import IsAdmin
from source.handlers import message_router, basic_router, callback_router, city_router,\
    admin_router, subscribe_router, transition_router, is_not_private
from source.utils.other import warning_database, alerts_message


# from source.keyboards.callback_data import Weather, Prediction, \
#     AddCity, AlertCall, Remove, Menu
# from source.utils.states import StateSet


async def connect_handlers(dispatcher: Dispatcher, scheduler, bot, connector):
    # middlewares
    dispatcher.callback_query.middleware.register(ChatActionMiddleware())
    dispatcher.message.middleware.register(ChatActionMiddleware())

    # Подключение router'ов
    dispatcher.message.register(is_not_private, IsNotPrivate())
    dispatcher.include_router(admin_router)
    dispatcher.include_router(city_router)
    dispatcher.include_router(subscribe_router)
    dispatcher.include_router(callback_router)
    dispatcher.include_router(basic_router)
    dispatcher.include_router(transition_router)
    dispatcher.include_router(message_router)

    next_hour = dt.now()+timedelta(minutes=60-dt.now().minute)

    # События по расписанию
    scheduler.add_job(alerts_message, trigger='interval', hours=1,
                      start_date=next_hour.replace(second=0),
                      kwargs={'bot': bot, 'db': connector})

    scheduler.add_job(warning_database, trigger='cron',
                      hour='23', minute='59', start_date=dt.now(),
                      kwargs={'bot': bot})

    # router.startup.register(set_default_commands)
    #
    # router.message.register(cmd_start, Command(commands=['start']))
    # router.message.register(cmd_help, Command(commands=['help']))
    # router.message.register(cmd_message, Command(commands='message'), IsAdmin())
    # router.message.register(call_alerts_message, Command('alerts'), IsAdmin())
    # router.message.register(upload_database, Command(commands=['db']), IsAdmin())
    #
    # router.message.register(set_city, F.text and StateSet.city)
    #
    # router.message.register(send_log, Command('log'), IsAdmin())
    #
    # router.callback_query.register(cmd_help, F.data == 'help')
    # router.callback_query.register(kb_set, AddCity.filter(), StateSet.city)
    # router.callback_query.register(weather_with_button, Weather.filter())
    # router.callback_query.register(city_kb, Remove.filter())
    # router.callback_query.register(call_city, Menu.filter())
    # router.callback_query.register(call_alerts, AlertCall.filter())
    # router.callback_query.register(call_prediction, Prediction.filter())


