from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.utils.states import StateAlerts
from core.keyboards.inline import menu
from core.keyboards.reply import cancel
from core.database.tables.Alert import Alert
from core.utils.other import get_weather
from core.database.Connector import Connector

router = Router()


@router.message(F.text and StateAlerts.subscribe)
async def second_step_alert(message: Message, state: FSMContext, connector: Connector):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.answer(f'Главное меню', reply_markup=menu())
    else:
        with connector.connector() as db:
            city = message.text.capitalize()
            try:  # Обработка ошибки если такого региона не существует
                checkout = get_weather(city, timezone=True)
                if checkout is None:
                    raise ValueError
                if db.query(Alert).where(
                        Alert.telegram_id == message.from_user.id).first() is None:
                    db.add(Alert(
                        telegram_id=message.from_user.id,
                        username=message.from_user.username,
                        city=city,
                        timezone=checkout
                    ))
                else:
                    db.query(Alert).where(
                        Alert.telegram_id == int(message.from_user.id)).update(
                        {
                            Alert.telegram_id: message.from_user.id,
                            Alert.city: city,
                            Alert.username: message.from_user.username,
                            Alert.timezone: checkout
                        }
                    )
                data = await state.get_data()
                call = data.get('call')
                await call.message.edit_text(
                    text='Вы подписаны на рассылку 🎉',
                    reply_markup=menu()
                )
                await state.clear()
            except ValueError:
                await message.answer(
                    f'Что-то пошло не так! \U0001F915'
                    f'\nНапишите "отмена", если передумали',
                    reply_markup=cancel()
                )
            finally:
                db.commit()
                await message.delete()
