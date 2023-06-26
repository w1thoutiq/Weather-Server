from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from source.utils.states import StateSet
from source.keyboards.inline import menu, add_city_menu
from source.keyboards.reply import cancel
from source.database.connector import Connector
from source.database.tables.User import User
from source.utils.other import get_weather
from source.keyboards.callback_data import AddCity

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
    city = data.get('city')+"\n"
    async with connector.connector() as db:
        async with db.begin():
            if action == 'add':
                cities = '\n'.join(await connector.cities_of_user(call.from_user.id))
                if city in cities:
                    await bot.edit_message_text(
                        chat_id=call.from_user.id,
                        message_id=call.message.message_id,
                        text=f'Этот город уже есть в списке'
                    )
                else:
                    cities_new = f'{cities}\n{city}'
                    new_value = await db.execute(select(User).where(User.telegram_id == call.from_user.id))
                    new_value.mappings().fetchone().get('User').city = cities_new
                    await bot.edit_message_text(
                        chat_id=call.from_user.id,
                        message_id=call.message.message_id,
                        text=f'<b>Город добавлен</b>',
                        reply_markup=menu()
                    )
            elif action == 'set':
                new_value = await db.execute(
                    select(User).where(User.telegram_id == call.from_user.id))
                new_value.mappings().fetchone().get('User').city = city
                await bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f'Город установлен!\nВаш регион: <b>{city}</b>',
                    reply_markup=menu()
                )
            await db.commit()
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
