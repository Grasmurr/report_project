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
from telegram_bot.repository.api_methods import get_all_events, get_ticket_by_number_or_type

import csv
import pandas as pd


import openpyxl
from io import BytesIO
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from . import dp
from telegram_bot.helpers import chat_backends
from telegram_bot.states import AdminStates
import tempfile





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
    await state.set_state(AdminStates.upload_data_in_format)
    event_name = message.text
    await state.update_data(event_name=event_name)
    await message.answer(text='Выберите формат, в котором хотите выгрузить данные:',
                         reply_markup=markup)

@dp.message(AdminStates.upload_data_in_format, F.text == 'Назад')
async def back_from_choosing_event_for_uploading_data(message: Message, state: FSMContext):
    await choose_event_for_uploading_data(message, state)

def filter_data_by_event(data, event):
    print (data)
    filtered_data = [item for item in data["data"] if item["event"] == event]
    if len(filtered_data) == 0:
        return "Для этого мероприятия нет билетов."
    return filtered_data
def convert_data_to_file(data, event, file_format):
    print (data)
    filtered_data = filter_data_by_event(data, event)

    if isinstance(filtered_data, str):
        print(filtered_data)
        return

    if file_format == ".csv":
        filename = f"{event}.csv"
        with open(filename, "w", newline="") as csvfile:
            fieldnames = filtered_data[0].keys()
            fieldnames_russian = {
                "id": "ID",
                "event": "Мероприятие",
                "ticket_number": "Номер билета",
                "ticket_holder_name": "Имя",
                "ticket_holder_surname": "Фамилия",
                "ticket_type": "Тип билета",
                "date_of_birth": "Дата рождения",
                "price": "Цена",
                "educational_program": "Образовательная программа",
                "educational_course": "Курс"
            }
            writer = csv.DictWriter(csvfile, fieldnames=[fieldnames_russian[field] for field in fieldnames])
            writer.writeheader()
            writer.writerows(
                [{fieldnames_russian[field]: item[field] for field in fieldnames} for item in filtered_data])
    elif file_format == ".xlsx":
        filename = f"{event}.xlsx"
        df = pd.DataFrame(filtered_data)
        df = df.rename(columns={
            "id": "ID",
            "event": "Мероприятие",
            "ticket_number": "Номер билета",
            "ticket_holder_name": "Имя",
            "ticket_holder_surname": "Фамилия",
            "ticket_type": "Тип билета",
            "date_of_birth": "Дата рождения",
            "price": "Цена",
            "educational_program": "Образовательная программа",
            "educational_course": "Курс"
        })
        df.to_excel(filename, index=False)
    else:
        print("Неподдерживаемый формат файла")

# @dp.message(AdminStates.upload_data_in_format, F.text == '.xlsx' or  F.text == '.csv')
# async def export_event_data(message: Message, state: FSMContext):
#     data = await state.get_data()
#     event = data['event_name']
#     file_format = message.text
#
#     tickets_data = await get_all_tickets()
#
#     convert_data_to_file(data=tickets_data, event=event, file_format=file_format)
#
#     tickets = [ticket for ticket in all_tickets['data'] if ticket['event'] == event_name]
#     if not tickets:
#         await message.answer("Для этого мероприятия нет билетов.")
#         return
#
#     markup = chat_backends.create_keyboard_buttons('Выгрузить в другом формате', 'Вернуться в меню админа')
#
#
#
#     await state.set_state(AdminStates.upload_data_in_format_final)

@dp.message(AdminStates.upload_data_in_format, F.text.in_(['.xlsx', '.csv']))
async def export_event_data(message: Message, state: FSMContext):

    data = await state.get_data()
    event = data['event_name']
    file_format = message.text

    tickets_data = await get_ticket_by_number_or_type(event=event)
    print (tickets_data)

    filename = convert_data_to_file(data=tickets_data, event=event, file_format=file_format)

    if isinstance(filename, str):
        markup = chat_backends.create_keyboard_buttons('Выбрать другое мероприятие', 'Вернуться в меню админа')
        await message.answer(filename, markup=markup)
        return

    with open(filename, 'rb') as file:
        markup = chat_backends.create_keyboard_buttons('Выгрузить в другом формате', 'Выбрать другое мероприятие', 'Вернуться в меню админа')
        await message.answer_document(file)
        await message.answer(text=f'Вот ваш файл в формате {file_format}', markup=markup)

    await state.set_state(AdminStates.upload_data_in_format_final)

@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
async def upload_data_in_another_format(message: Message, state: FSMContext):
    await choose_format_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Вернуться в меню админа')
async def back_from_upload_data_in_format(message: Message, state: FSMContext):
    await admin_menu(message, state)
