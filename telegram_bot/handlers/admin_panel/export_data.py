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
from telegram_bot.repository.api_methods import get_all_events, get_all_tickets

import csv

import openpyxl
from io import BytesIO
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from . import dp
from telegram_bot.helpers import chat_backends
from telegram_bot.states import AdminStates
from telegram_bot.repository.api_methods import get_tickets_by_event
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

@dp.message(AdminStates.upload_data_in_format, F.text.in_(['.xlsx', '.csv']))
async def export_event_data(message: Message, state: FSMContext):
    data = await state.get_data()
    event_name = data['event_name']
    export_format = message.text

    all_tickets = await get_all_tickets()
    tickets = [ticket for ticket in all_tickets['data'] if ticket['event'] == event_name]
    if not tickets:
        await message.answer("Для этого мероприятия нет билетов.")
        return

    markup = chat_backends.create_keyboard_buttons('Выгрузить в другом формате', 'Вернуться в меню админа')

    if export_format == '.csv':
        csv_data = []
        for ticket in tickets:
            csv_data.append([ticket['ticket_number'], ticket['ticket_holder_name'],
                             ticket['ticket_holder_surname'], ticket['ticket_type']])

        csv_buffer = BytesIO()
        writer = csv.writer(csv_buffer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Номер билета', 'Имя', 'Фамилия', 'Тип билета'])
        writer.writerows(csv_data)
        csv_buffer.seek(0)

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_buffer.getvalue())
            temp_file_path = temp_file.name

        await message.answer_document(temp_file_path,
                                      caption=f"Вот файл с данными о билетах на мероприятие {hcode(event_name)}"
                                              f" в формате.csv", reply_markup=markup)

    elif export_format == '.xlsx':
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(['Номер билета', 'Имя', 'Фамилия', 'Тип билета'])

        for ticket in tickets:
            worksheet.append([ticket['ticket_number'], ticket['ticket_holder_name'],
                              ticket['ticket_holder_surname'], ticket['ticket_type']])

        xlsx_buffer = BytesIO()
        workbook.save(xlsx_buffer)
        xlsx_buffer.seek(0)
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            temp_file.write(xlsx_buffer.getvalue())
            temp_file_path = temp_file.name

        await message.answer_document(temp_file_path,
                                      caption=f"Вот файл с данными о билетах на мероприятие {hcode(event_name)} "
                                              f"в формате .xlsx", reply_markup=markup)

    await state.set_state(AdminStates.upload_data_in_format_final)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
async def upload_data_in_another_format(message: Message, state: FSMContext):
    await choose_format_for_uploading_data(message, state)


@dp.message(AdminStates.upload_data_in_format_final, F.text == 'Вернуться в меню админа')
async def back_from_upload_data_in_format(message: Message, state: FSMContext):
    await admin_menu(message, state)
