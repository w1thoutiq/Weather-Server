from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from core.utils.graph import get_city_set
from core.utils.other import *
from core.keyboards.inline import *
from core.utils.states import *
from core.utils import prediction


router = Router()


@router.callback_query(F.data.startswith('weather_'))
async def weather_with_button(call: CallbackQuery, bot: Bot):
    await call.answer()
    city = call.data.split('weather_')[1]
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


@router.callback_query(F.data.startswith('city_'))
async def city_kb(call: CallbackQuery, bot: Bot):
    city = call.data.split('city_')[1]
    if city == 'cancel':
        await bot.delete_message(message_id=call.message.message_id,
                                 chat_id=call.from_user.id)
    else:
        with create_session() as db:
            cities = db.query(User.city).where(
                User.id == int(call.from_user.id)
            ).first()[0].replace(city + ', ', '')
            db.query(User).where(User.id == int(call.from_user.id)).update(
                {User.city: cities}
            )
            cities = cities.split(', ')
            await bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text=f'Какой еще регион хотите удалить?',
                reply_markup=get_button_with_city(cities))
            await call.answer('Удалил регион {}'.format(city), show_alert=True)
            db.commit()


@router.callback_query(F.data.startswith('menu_'))
async def call_city(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(message_id=call.message.message_id)
    await call.answer()
    action = call.data.split('menu_')[1]
    with create_session() as db:
        if action == 'change':
            city = db.query(User.city).where(
                User.id == int(call.from_user.id)
            ).first()[0].split(', ')
            await bot.send_message(chat_id=call.from_user.id,
                                   text=f'Ваши регионы:',
                                   reply_markup=get_button_with_city(city))
        elif action == 'add':
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=f'Отправь свой населенный пункт',
                reply_markup=cancel()
            )
            await state.set_state(StateSet.city)
        elif action == 'my_city':
            await my_city(call, bot=bot)
        elif action == 'alerts':
            if db.query(Alert).where(Alert.id == call.from_user.id).first():
                city = db.query(Alert.city).where(Alert.id == call.from_user.id).first()[0]
                await call.message.edit_text(
                    text="Меню рассылки:\n\r"
                         "<strong>Вы подписаны \U00002705\n"
                         "Ваш регион - {}</strong>".format(city),
                    reply_markup=menu_of_alerts(subscribe=True),
                    parse_mode='HTML')
            elif db.query(Alert).where(
                    Alert.id == call.from_user.id
            ).first() is None:
                await call.message.edit_text(
                    text="Меню рассылки:\n\r"
                         "<strong>Вы не подписаны</strong> \U0000274C",
                    reply_markup=menu_of_alerts(),
                    parse_mode='HTML'
                )
        elif action == 'graph':
            await call.message.answer(
                'Выбери регион',
                reply_markup=graph_keyboard(get_city_set())
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


@router.callback_query(F.data.startswith('alerts_'))
async def call_alerts(call: CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await call.answer()
    action = call.data.split('alerts_')[1]
    if action == 'unsubscribe':
        with create_session() as db:
            db.query(Alert).where(Alert.id == int(call.from_user.id)).delete()
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


@router.callback_query(F.data.startswith('prediction_'))
@flags.chat_action('upload_photo')
async def call_prediction(call: CallbackQuery):
    await call.answer()
    action = call.data.split('_')[1]
    try:
        with create_session() as db:
            city = db.query(Alert.city).where(Alert.id == call.from_user.id).first()[0]
        if action == 'today':
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
        elif action == 'tomorrow':
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
