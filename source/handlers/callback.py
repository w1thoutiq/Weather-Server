from datetime import datetime, timedelta

from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, flags
from aiogram.types import CallbackQuery, FSInputFile

# from source.keyboards.Data import Menu, AlertCall, Weather, Prediction, Remove
from source.utils.other import get_weather, get_weather_for_cities, my_city
from source.keyboards.inline import *
from source.utils.states import *
from source.utils import prediction
from source.database.connector import Connector
from source.database.tables.Alert import Alert
from source.keyboards.reply import cancel

router = Router()


@router.callback_query(Weather.filter())
async def weather_with_button(
        call: CallbackQuery, bot: Bot, callback_data: Weather
):
    await call.answer()
    city = callback_data.city
    get_weather(city)
    if city == 'cancel':
        await bot.delete_message(message_id=call.message.message_id,
                                 chat_id=call.message.chat.id)
    elif city == 'all':
        await get_weather_for_cities(
            user_id=call.from_user.id,
            bot=bot,
            chat_id=call.from_user.id
        )
    else:
        await bot.send_message(chat_id=call.message.chat.id,
                               text=get_weather(city),
                               parse_mode='HTML')


@router.callback_query(Remove.filter())
async def city_kb(
        call: CallbackQuery,
        bot: Bot,
        connector: Connector,
        callback_data: Remove
):
    city = callback_data.city
    if city == 'cancel':
        await bot.delete_message(message_id=call.message.message_id,
                                 chat_id=call.from_user.id)
    else:
        await connector.remove_city(user=call.from_user.id, city=f'{city}')
        await bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.from_user.id,
            text=f'Какой еще регион хотите удалить?',
            reply_markup=get_button_with_city(
                await connector.cities_of_user(call.from_user.id)
            )
        )
        await call.answer(f'Удалил регион {city}', show_alert=True)


@router.callback_query(Menu.filter())
async def call_city(
        call: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        connector: Connector,
        callback_data: Menu
):
    action = callback_data.action
    await state.update_data(message_id=call.message.message_id)
    await call.answer()
    if action == 'change':
        city = await connector.cities_of_user(call.from_user.id)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f'Ваши регионы для удаления:',
            reply_markup=get_button_with_city(city)
        )
    elif action == 'add':
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Отправь свой населенный пункт',
            reply_markup=cancel()
        )
        await state.set_state(StateSet.city)
    elif action == 'my_city':
        await my_city(call, bot=bot, connector=connector)
    elif action == 'alerts':
        if await connector.get_status_alert(call.from_user.id):
            # print(1)
            city = await connector.alert_city(call.from_user.id)
            await call.message.edit_text(
                text="Меню рассылки:\n\r"
                     "<strong>Вы подписаны \U00002705\n"
                     "Ваш регион - {}</strong>".format(city),
                reply_markup=menu_of_alerts(subscriber=True),
                parse_mode='HTML')
        else:
            await call.message.edit_text(
                text="Меню рассылки:\n\r"
                     "<strong>Вы не подписаны</strong> \U0000274C",
                reply_markup=menu_of_alerts(),
                parse_mode='HTML'
            )
    elif action == 'graph':
        await call.message.answer(
            'Выбери регион',
            reply_markup=graph_keyboard(await connector.cities_of_user(call.from_user.id))
        )
    elif action == 'prediction':
        await call.message.edit_text(
            text='<b>Если вы не подписаны на рассылку, я не пришлю вам '
                 'прогноз погоды.</b>\n\rВыберите прогноз:',
            reply_markup=prediction_menu()
        )


@router.callback_query(F.data.startswith('graph_'))
async def send_graph(call: CallbackQuery, bot: Bot):
    await call.answer()
    city = call.data.split('graph_')[1]
    try:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=FSInputFile(
                f'Graph\\{city}\\{datetime.now().date()-timedelta(days=1)}.png'
            ),
            caption=f'График погоды города - <b>{city}</b>'
                    f' за <b>{datetime.now().date()-timedelta(days=1)}</b>'
        )
    except TelegramNetworkError:
        await call.message.answer('График не найден 😐')


@router.callback_query(AlertCall.filter())
async def call_alerts(
        call: CallbackQuery,
        state: FSMContext,
        connector: Connector,
        callback_data: AlertCall
):
    action = callback_data.action
    await state.update_data(call=call)
    await call.answer()
    if action == 'unsubscribe':
        with connector.connector() as db:
            db.query(Alert).where(Alert.telegram_id == int(call.from_user.id)).delete()
            db.commit()
        await call.message.edit_text(
            text='Удалил вас из рассылки',
            reply_markup=menu()
        )
    elif action == 'subscribe':
        await call.message.edit_text(
            text=f'Отправь регион для рассылки',
        )
        await state.set_state(StateAlerts.subscribe)
    elif action == 'cancel':
        await call.message.edit_text(
            text='Главное меню',
            reply_markup=menu()
        )


@flags.chat_action('upload_photo')
@router.callback_query(Prediction.filter())
async def call_prediction(
        call: CallbackQuery,
        connector: Connector,
        callback_data: Prediction
):
    await call.answer()
    day = callback_data.day
    try:
        city = await connector.alert_city(call.from_user.id)
        if day == 'today':
            await prediction.get_weather(city, tomorrow=False)
            await call.message.delete()
            await call.message.answer_photo(
                photo=FSInputFile(f'Bar\\{city}\\{datetime.now().date()}.png'),
                caption="<b>🟢 - Облачно\n"
                        "🔵 - Дождливая погода\n"
                        "🟡 - Ясно</b>"
            )
            await call.message.answer(
                'Прогноз на сегодня',
                reply_markup=menu(),
                disable_notification=True
            )
            return
        elif day == 'tomorrow':
            await prediction.get_weather(city, tomorrow=True)
            await call.message.delete()
            await call.message.answer_photo(
                photo=FSInputFile(
                    f'Bar\\{city}\\{(datetime.now()+timedelta(days=1)).date()}.png'
                ),
                caption="<b>🟢 - Облачно\n"
                        "🔵 - Дождливая погода\n"
                        "🟡 - Ясно</b>"
            )
            await call.message.answer(
                'Прогноз на завтра',
                reply_markup=menu(),
                disable_notification=True
            )
            return
    except TypeError:
        await call.message.answer(
            'Возможно вы не подписаны на рассылку.',
            reply_markup=menu_of_alerts()
        )
    except Exception:
        await call.message.answer('Что-то пошло не так.')
