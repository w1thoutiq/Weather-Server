# from aiogram import Router, F
# from aiogram.filters import Command
#
# from source.middlewares.filters import IsAdmin
# from source.handlers import *
# from source.keyboards.callback_data import Weather, Prediction, \
#     AddCity, AlertCall, Remove, Menu
# from source.utils.states import StateSet
#
#
# async def routers(router: Router):
#     router.startup.register(set_default_commands)
#
#     router.message.register(cmd_start, Command(commands=['start']))
#     router.message.register(cmd_help, Command(commands=['help']))
#     router.message.register(cmd_message, Command(commands='message'), IsAdmin())
#     router.message.register(call_alerts_message, Command('alerts'), IsAdmin())
#     router.message.register(upload_database, Command(commands=['db']), IsAdmin())
#
#     router.message.register(set_city, F.text and StateSet.city)
#
#     router.message.register(send_log, Command('log'), IsAdmin())
#
#     router.callback_query.register(cmd_help, F.data == 'help')
#     router.callback_query.register(kb_set, AddCity.filter(), StateSet.city)
#     router.callback_query.register(weather_with_button, Weather.filter())
#     router.callback_query.register(city_kb, Remove.filter())
#     router.callback_query.register(call_city, Menu.filter())
#     router.callback_query.register(call_alerts, AlertCall.filter())
#     router.callback_query.register(call_prediction, Prediction.filter())
#
#
