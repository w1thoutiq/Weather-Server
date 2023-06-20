from aiogram.filters.callback_data import CallbackData


class Menu(CallbackData, prefix='menu'):
    action: str


class AlertCall(CallbackData, prefix='alert'):
    action: str


class Weather(CallbackData, prefix='weather'):
    city: str


class Prediction(CallbackData, prefix='prediction'):
    day: str


class Remove(CallbackData, prefix='remove'):
    city: str


class AddCity(CallbackData, prefix='add_city'):
    action: str
