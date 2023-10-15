from telegram_bot.loader import dp
from aiogram.types import \
    (Message
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates


@dp.message(F.text == '/admin')
async def admin_menu(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                   "Оформить возврат",
                                                   "Cделать выгрузку данных",
                                                   "Назад")
    await state.set_state(AdminStates.main)
    await message.answer('Добро пожаловать в админ-панель', reply_markup=markup)