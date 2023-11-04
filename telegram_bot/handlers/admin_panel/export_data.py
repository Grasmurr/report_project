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
from aiogram.types import InputFile

from telegram_bot.states import AdminStates

from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu
from telegram_bot.repository.api_methods import get_all_events, get_ticket_by_number_or_type

import csv
import pandas as pd
import io
import tempfile, os

import openpyxl
from io import BytesIO
from aiogram.types import Message
from aiogram.utils.markdown import hcode
import tempfile

from . import dp
from telegram_bot.helpers import chat_backends
from telegram_bot.states import AdminStates


@dp.message(AdminStates.main, F.text == "Cделать выгрузку данных")
async def choose_event_for_uploading_data(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.upload_data)
    await message.answer(text='Выберите мероприятие, данные которого вы хотите выгрузить',
                         reply_markup=markup)


@dp.message(AdminStates.upload_data, F.text == 'Назад')
async def back_from_uploading_data(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.upload_data, F.text != 'Назад')
async def choose_format_for_uploading_data(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('.xlsx', '.csv', 'Назад')

    event_name = message.text
    await state.update_data(event_name=event_name)

    data = await get_ticket_by_number_or_type(event=event_name)
    data = data['data']

    if event_name == "Выгрузить в другом формате":
        await message.answer(text='Выберите формат, в котором хотите выгрузить данные:',
                             reply_markup=markup)
        await state.set_state(AdminStates.upload_data_in_format)

    elif data == []:
        markup = chat_backends.create_keyboard_buttons('Выбрать другое мероприятие',
                                                       'Вернуться в меню админа')
        await message.answer(text="На это мероприятие не было куплено билетов",
                             markup=markup)
        await state.set_state(AdminStates.upload_data_in_format_final)

    else:
        await message.answer(text='Выберите формат, в котором хотите выгрузить данные:',
                             reply_markup=markup)
        await state.set_state(AdminStates.upload_data_in_format)


@dp.message(AdminStates.upload_data_in_format, F.text == 'Назад')
async def back_from_choosing_event_for_uploading_data(message: Message, state: FSMContext):
    await choose_event_for_uploading_data(message, state)


def create_table(data, event, file_format):
    columns = {
        "id": "ID",
        "event": "Мероприятие",
        "ticket_number": "Номер билета",
        "ticket_holder_name": "Имя",
        "ticket_holder_surname": "Фамилия",
        "ticket_type": "Тип билета",
        "date_of_birth": "Дата рождения",
        "price": "Цена",
        "educational_program": "Образовательная программа",
        "educational_course": "Курс",
        "phone_number": "Номер телефона"
    }

    df = pd.DataFrame.from_records(data)
    df = df.rename(columns=columns)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    file_path = event + file_format

    if file_format == ".xlsx":
        df.to_excel(file_path, index=False)
    elif file_format == ".csv":
        df.to_csv(file_path, index=False)
    else:
        print("Unsupported file format")
        return

    return file_path


@dp.message(AdminStates.upload_data_in_format, F.text.in_(['.xlsx', '.csv']))
async def export_event_data(message: Message, state: FSMContext):
    data = await state.get_data()
    event = data['event_name']
    file_format = message.text

    data = await get_ticket_by_number_or_type(event=event)
    data = data['data']

    file_path = create_table(data, event, file_format)

    markup = chat_backends.create_keyboard_buttons('Выгрузить в другом формате', 'Выбрать другое мероприятие',
                                                   'Вернуться в меню админа')
    caption = f"Вот ваш файл в формате {file_format}"
    with open(file_path, "rb") as file:
        await message.answer_document(document=BufferedInputFile(file.read(), filename=f'{event}{file_format}*'),
                                      caption=caption, reply_markup=markup)


    os.remove(file_path)

    await state.set_state(AdminStates.upload_data_in_format_final)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
async def upload_data_in_another_format(message: Message, state: FSMContext):
    await choose_format_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выбрать другое мероприятие')
async def upload_data_of_another_event(message: Message, state: FSMContext):
    await choose_event_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Вернуться в меню админа')
async def back_from_upload_data_in_format(message: Message, state: FSMContext):
    await admin_menu(message, state)
