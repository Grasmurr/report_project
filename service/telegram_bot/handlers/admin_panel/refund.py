from service.telegram_bot.loader import dp, bot
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
from service.telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from service.telegram_bot.states import AdminStates


from service.telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu


@dp.message(AdminStates.main, F.text == 'Оформить возврат')
async def choose_event_for_ticket_refund (message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Все счастливы', 'Все несчастны', 'Назад')
    await state.set_state(AdminStates.ticket_refund)
    await message.answer(text='Выберите мероприятие для которого вы хотите оформить возврат билета?',
                         reply_markup=markup)

# TODO: здесь должен быть код для возвратов


@dp.message(AdminStates.ticket_refund, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await admin_menu(message, state)