from aiogram.utils.keyboard import InlineKeyboardBuilder
from source.keyboards.callback_data import Menu, AlertCall, Weather, Prediction, Remove, AddCity


def menu_of_alerts(subscriber: bool = False):
    builder = InlineKeyboardBuilder()
    if subscriber:
        builder.button(text='Поменять', callback_data=AlertCall(action='subscribe'))
    else:
        builder.button(text='Подписаться', callback_data=AlertCall(action='subscribe'))
    builder.button(text='Отписаться', callback_data=AlertCall(action='unsubscribe'))
    builder.button(text=f'Назад', callback_data=AlertCall(action=f'cancel'))
    builder.adjust(2, 1)
    return builder.as_markup()


def get_button_with_city(cities):
    markup = InlineKeyboardBuilder()
    if len(cities) % 2 == 0:
        lst = [2 for i in range(0, len(cities) + 2, 2)]
    else:
        lst = [2 for i in range(0, len(cities)-2, 2)]
        lst.append(1)
        lst.append(2)
    for city in cities:
        markup.button(text=city, callback_data=Remove(city=city))
    markup.button(text=f'Назад', callback_data=Remove(city='cancel'))
    markup.adjust(*lst)
    return markup.as_markup()
    # buttons = [[InlineKeyboardButton(
    #     text=city, callback_data=f' remove_{city}'
    # )] for city in cities]
    # buttons.append([InlineKeyboardButton(
    #     text=f'Назад', callback_data=f' remove_cancel')])
    # return InlineKeyboardMarkup(inline_keyboard=buttons)


def weather_btn(cities: list):
    markup = InlineKeyboardBuilder()
    if len(cities) % 2 == 0:
        lst = [2 for i in range(0, len(cities) + 2, 2)]
    else:
        lst = [2 for i in range(0, len(cities)-2, 2)]
        lst.append(1)
        lst.append(2)
    for city in cities:
        markup.button(text=city, callback_data=Weather(city=city))
    markup.button(
        text=f'Все регионы', callback_data=Weather(city='all')
    ).button(text=f'Назад', callback_data=Weather(city='cancel'))
    markup.adjust(*lst)
    return markup.as_markup()


def menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='Удалить регионы', callback_data=Menu(action='change'))
    markup.button(text='Добавить регионы', callback_data=Menu(action='add'))
    markup.button(text='Ваши регионы', callback_data=Menu(action='my_city'))
    markup.button(text='Рассылка', callback_data=Menu(action='alerts'))
    markup.button(text='Прогноз погоды', callback_data=Menu(action='prediction'))
    # markup.add(
    # InlineKeyboardButton(text='Мониторинг погоды', callback_data='menu_graph')
    # )
    markup.adjust(2)
    return markup.as_markup()


def graph_keyboard(cities):
    markup = InlineKeyboardBuilder()
    for city in cities:
        markup.button(text=city, callback_data=f'graph_{city}')
    markup.adjust(2)
    markup.button(text=f'Назад', callback_data=Weather(city='cancel'))
    return markup.as_markup()


def add_city_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='Установить единственным', callback_data=AddCity(action='set')),
    markup.button(text='Добавить регион', callback_data=AddCity(action='add'))
    markup.adjust(2)
    return markup.as_markup()


def admin():
    buttons = InlineKeyboardBuilder()
    buttons.button(text='Вавилон', url='https://t.me/w1thoutiq')
    return buttons.as_markup()


def mark():
    markup = InlineKeyboardBuilder()  # Создаём макеты для отображения кнопок
    markup.button(text='help', callback_data='help')  # Добавляем кнопку help
    # markup.button(
    #     text="it's YouTube!", web_app=WebAppInfo(
    #         url='https://'
    #     )
    # )
    return markup.as_markup()


def prediction_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='До конца дня', callback_data=Prediction(day='today'))
    markup.button(text='На завтра', callback_data=Prediction(day='tomorrow'))
    markup.button(text=f'Назад', callback_data=AlertCall(action=f'cancel'))
    markup.adjust(2)
    return markup.as_markup()


# def admin_menu():
#     markup = InlineKeyboardBuilder()
#     markup.button(text="Прислать базу данных", callback_data=CallAdmin(data='db'))
#     markup.button(text='Рассылка "alert"', callback_data=CallAdmin(data='alert'))
#     markup.button(text='Рассылка "message"', callback_data=CallAdmin(data='message'))
#     markup.button(text="Все пользователи", callback_data=CallAdmin(data='users'))
#     markup.adjust(1)
#     return markup.as_markup()
