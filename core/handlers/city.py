from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.utils.states import StateSet
from core.keyboards.inline import menu, add_city_menu
from core.keyboards.reply import cancel
from core.database.Connector import Connector
from core.database.tables.User import User
from core.utils.other import get_weather
from core.keyboards.callback_data import AddCity

router = Router()


@router.callback_query(AddCity.filter(), StateSet.city)
async def kb_set(
        call: CallbackQuery,
        state: FSMContext,
        bot: Bot,
        connector: Connector,
        callback_data: AddCity
):
    await call.answer()
    action = callback_data.action
    data = await state.get_data()
    city = data.get('city')+", "
    with connector.connector() as db:
        if action == 'add':
            cities = ', '.join(await connector.cities_of_user(call.from_user.id))
            if city in cities:
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f'Этот город уже есть в списке'
                )
            else:
                cities = f'{cities}{city}'
                db.query(User).where(User.telegram_id == int(call.from_user.id)).update({
                    User.city: cities, User.status: 'member'
                })
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f'<b>Город добавлен</b>',
                    reply_markup=menu()
                )
            db.commit()
        elif action == 'set':
            db.query(User).where(User.telegram_id == int(call.from_user.id)).update({
                User.city: city, User.status: 'member'
            })
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f'Город установлен!\nВаш регион: <b>{city}</b>',
                reply_markup=menu()
            )
        db.commit()
        await state.clear()


@router.message(F.text and StateSet.city)
async def set_city(message: Message, state: FSMContext, connector: Connector):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer(f'Главное меню', reply_markup=menu())
    else:
        city = message.text.capitalize()
        if city in await connector.cities_of_user(message.from_user.id):
            await message.answer('Этот город уже добавлен')
            return
        try:  # Обработка ошибки если такого региона не существует
            if get_weather(city) is None:
                raise ValueError
            await state.update_data(city=city)
            await message.answer(f'Что ты хочешь сделать с этим регионом?',
                                 reply_markup=add_city_menu())
        except ValueError:
            await message.reply(
                f'Что-то пошло не так! \U0001F915'
                f'\nНапишите "отмена", если передумали',
                reply_markup=cancel())
