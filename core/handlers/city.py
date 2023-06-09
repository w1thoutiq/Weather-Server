from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states import StateSet
from core.keyboards.inline import menu, add_city_menu
from core.keyboards.reply import cancel
from core.utils.connect_db import User
from core.utils.other import get_weather
from core.utils.session_db import create_session

router = Router()


@router.callback_query(F.data.startswith('kb_'), StateSet.city)
async def kb_set(call, state: FSMContext, bot: Bot):
    await call.answer()
    action = call.data.split('kb_')[1]
    data = await state.get_data()
    city = data.get('city') + ', '
    with create_session() as db:
        if action == 'add':
            cities = db.query(User.city).where(
                User.id == int(call.from_user.id)
            ).first()[0]
            if city in cities:
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f'Этот город уже есть в списке'
                )
            else:
                cities = f'{cities}{city}'
                db.query(User).where(User.id == int(call.from_user.id)).update({
                    User.city: cities, User.active: True
                })
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f'Город добавлен'
                )
            db.commit()
        elif action == 'set':
            db.query(User).where(User.id == int(call.from_user.id)).update({
                    User.city: city, User.active: True
                })
            await bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f'Город установлен!\nВаш регион: {city[:-2:]}')
        db.commit()
        await state.clear()


@router.message(F.text and StateSet.city)
async def set_city(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer(f'Главное меню', reply_markup=menu())
    else:
        city = message.text.capitalize()
        try:  # Обработка ошибки если такого региона не существует
            if get_weather(city) is None:
                raise ValueError
            await state.update_data(city=city)
            await message.answer(f'Что ты хочешь сделать с этим регионом?',
                                 reply_markup=add_city_menu()
                                 )
        except ValueError:
            await message.reply(
                f'Что-то пошло не так! \U0001F915'
                f'\nНапишите "отмена", если передумали',
                reply_markup=cancel()
                                )
