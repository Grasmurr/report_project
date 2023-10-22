from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository import api_methods

@dp.message(F.text == '/admin')
async def admin_menu(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                   "Оформить возврат",
                                                   "Cделать выгрузку данных",
                                                   "Назад")
    await state.set_state(AdminStates.main)
    await message.answer('Добро пожаловать в админ-панель', reply_markup=markup)

    tickets = await api_methods.get_all_tickets()
    print(tickets)