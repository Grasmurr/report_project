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


@dp.message(AdminStates.main, F.text == "Cделать выгрузку данных")
async def choose_event_for_uploading_data(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Все счастливы', 'Все несчастны', 'Назад')
    await state.set_state(AdminStates.upload_data)
    await message.answer(text='Выберите мероприятие, данные которого вы хотите выгрузить',
                         reply_markup=markup)


@dp.message(AdminStates.upload_data, F.text != 'Назад')
async def choose_format_for_uploading_data(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('.xlsx', '.csv', 'Назад')
    await state.set_state(AdminStates.upload_data_in_format)
    await message.answer(text='Выберите формат, в котором хотите выгрузить данные:',
                         reply_markup=markup)


@dp.message(AdminStates.upload_data)
async def back_from_uploading_data(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.upload_data_in_format, F.text == 'Назад')
async def back_from_choosing_event_for_uploading_data(message: Message, state: FSMContext):
    await choose_event_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format)
async def choose_event_for_ticket_refund(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Выгрузить в другом формате', 'Вернуться в меню админа')
    await state.set_state(AdminStates.upload_data_in_format_final)
    await message.answer(text=f'Вот ваш файл в формате {message.text}',
                         reply_markup=markup)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
async def upload_data_in_another_format(message: Message, state: FSMContext):
    await choose_format_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Вернуться в меню админа')
async def back_from_upload_data_in_format(message: Message, state: FSMContext):
    await admin_menu(message, state)
