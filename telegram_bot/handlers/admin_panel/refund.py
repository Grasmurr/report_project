from telegram_bot.loader import dp, bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import \
    (Message,
     CallbackQuery,
     KeyboardButton,
     ReplyKeyboardMarkup,
     InlineKeyboardMarkup,
     InlineKeyboardButton,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from telegram_bot.states import AdminStates


from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

from telegram_bot.repository import api_methods


@dp.message(AdminStates.main, F.text == 'Оформить возврат')
async def ticket_refund_start(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.choose_event_to_refund)
    await message.answer(text='Выберите мероприятие для которого вы хотите оформить возврат билета?',
                         reply_markup=markup)


@dp.message(AdminStates.choose_event_to_refund)
async def choose_event_for_ticket_refund(message: Message, state: FSMContext):
    ans = message.text
    if ans == 'Назад':
        await admin_menu(message)
    else:
        await message.answer('Хорошо! Выберите тип билета, который вы хотите вернуть:')



@dp.message(AdminStates.ticket_refund, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await admin_menu(message, state)
