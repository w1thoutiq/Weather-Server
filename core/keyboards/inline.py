from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_of_alerts(subscribe: bool = False):
    builder = InlineKeyboardBuilder()
    if subscribe:
        builder.button(text='Поменять', callback_data='alerts_subscribe')
    else:
        builder.button(text='Подписаться', callback_data='alerts_subscribe')
    builder.button(text='Отписаться', callback_data='alerts_unsubscribe')
    builder.button(text=f'Назад', callback_data=f'alerts_cancel')
    builder.adjust(2, 1)
    return builder.as_markup()


def get_button_with_city(cities):
    buttons = [[InlineKeyboardButton(
        text=city, callback_data=f'city_{city}'
    )] for city in cities]
    buttons.append([InlineKeyboardButton(
        text=f'Назад', callback_data=f'city_cancel')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def weather_btn(cities):
    markup = InlineKeyboardBuilder()
    for city in cities:
        markup.add(InlineKeyboardButton(
            text=city,
            callback_data=f'weather_{city}'))
    markup.adjust(1)
    markup.add(InlineKeyboardButton(
        text=f'Все регионы', callback_data=f'weather_all'
    ), InlineKeyboardButton(
        text=f'Назад', callback_data=f'weather_cancel'
    ))
    return markup.as_markup()


def menu():
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(
        text='Удалить регионы', callback_data='menu_change'))
    markup.add(InlineKeyboardButton
               (text='Добавить регионы', callback_data='menu_add'))
    markup.add(InlineKeyboardButton(
        text='Ваши регионы', callback_data='menu_my_city'))
    markup.add(InlineKeyboardButton
               (text='Рассылка', callback_data='menu_alerts'))
    markup.add(InlineKeyboardButton(
        text='Прогноз погоды', callback_data='menu_prediction'))
    # markup.add(InlineKeyboardButton(
    #     text='Мониторинг погоды', callback_data='menu_graph'))
    markup.adjust(2)
    return markup.as_markup()


def graph_keyboard(cities):
    markup = InlineKeyboardBuilder()
    for city in cities:
        markup.add(InlineKeyboardButton(
            text=city, callback_data=f'graph_{city}'))
    markup.add(InlineKeyboardButton(
        text=f'Назад', callback_data=f'weather_cancel'))
    markup.adjust(1)
    return markup.as_markup()


def add_city_menu():
    markup = InlineKeyboardBuilder()
    markup.add(
        InlineKeyboardButton(
            text='Установить единственным', callback_data='kb_set'),
        InlineKeyboardButton(
            text='Добавить регион', callback_data='kb_add'))
    return markup.as_markup()


def admin():
    buttons = InlineKeyboardBuilder()
    buttons.add(InlineKeyboardButton(
        text='Вавилон', url='https://t.me/w1thoutiq'
    ))
    return buttons.as_markup()


def mark():
    markup = InlineKeyboardBuilder()  # Создаём макеты для отображения кнопок
    markup.add(InlineKeyboardButton(
        text='help', callback_data='help'
    ))  # Добавляем кнопку help
    return markup.as_markup()


def prediction_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='До конца дня', callback_data='prediction_today')
    markup.button(text='На завтра', callback_data='prediction_tomorrow')
    markup.button(text=f'Назад', callback_data=f'alerts_cancel')
    markup.adjust(2)
    return markup.as_markup()
