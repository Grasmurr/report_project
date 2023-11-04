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

from telegram_bot.gdrive.api_methods import update_gdrive

from telegram_bot.repository import api_methods


@dp.message(AdminStates.main, F.text == 'Оформить возврат')
async def ticket_refund_start(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.choose_event_to_refund)
    await message.answer(text='Выберите мероприятие для которого вы хотите оформить возврат билета:',
                         reply_markup=markup)


@dp.message(AdminStates.choose_event_to_refund, F.text == "Назад")
async def ticket_refund_choose_event_back(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.choose_event_to_refund)
async def ticket_refund_choose_type(message: Message, state: FSMContext):
    # TODO: Проверка что это не случайное нажатие
    event_to_refund = message.text
    exists = await api_methods.get_event(event_to_refund)
    if exists:
        await state.update_data(event_to_refund=event_to_refund)
        await state.set_state(AdminStates.enter_ticket_type_to_refund)
        markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Назад')
        await message.answer(text='Выберите тип билета, который вы хотите вернуть:', reply_markup=markup)
    else:
        events = await api_methods.get_all_events()
        event_names = [event['name'] for event in events['data']]
        markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
        await message.answer(text='Кажется, вы случайно нажали не на ту кнопку. Выберите мероприятие из списка кнопок:',
                             reply_markup=markup)


@dp.message(AdminStates.enter_ticket_type_to_refund, F.text == "Назад")
async def ticket_type_choose_event_back(message: Message, state: FSMContext):
    await ticket_refund_start(message, state)


@dp.message(AdminStates.enter_ticket_type_to_refund)
async def ticket_refund_choose_event(message: Message, state: FSMContext):
    type_to_refund = message.text
    if type_to_refund in ['Обычный', 'Прайм']:
        await state.update_data(type_to_refund=type_to_refund)
        await state.set_state(AdminStates.enter_ticket_number)
        await message.answer(text='Пожалуйста, введите номер билета, который вы хотите вернуть:',
                             reply_markup=ReplyKeyboardRemove())
    else:
        markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Назад')
        await message.answer(text='Кажется, вы случайно нажали не на ту кнопку. Выберите тип билета из списка кнопок:',
                             reply_markup=markup)


@dp.message(AdminStates.enter_ticket_number, F.text == 'Назад')
async def back_to_ticket_type(message: Message, state: FSMContext):
    await ticket_type_choose_event_back(message, state)


@dp.message(AdminStates.enter_ticket_number)
async def handle_ticket_number(message: Message, state: FSMContext):
    number_to_refund = message.text
    try:
        number_to_refund = int(number_to_refund)
    except:
        await message.answer('Кажется, вы ввели не номер билета! Пожалуйста, введите номер цифрами. Например: 150')
        # TODO: Сделать проверку на то, что этот билет есть в базе
    data = await state.get_data()

    exists = await api_methods.get_ticket_by_number_or_type(event=data['event_to_refund'],
                                                            ticket_number=number_to_refund,
                                                            ticket_type=data['type_to_refund'])
    print(exists)
    if exists['data']:
        id_data = exists
        await state.update_data(number_to_refund=number_to_refund)
        markup = chat_backends.create_keyboard_buttons('Продолжить', 'Назад')

        name = id_data['data'][0]['ticket_holder_name']
        surname = id_data['data'][0]['ticket_holder_surname']

        await message.answer(f'Вы хотите вернуть билет №{number_to_refund}.\n'
                             f'\nИмя: {name}\nФамилия: {surname}\n'
                             f'Тип билета: {data["type_to_refund"]} \n\nПродолжить?', reply_markup=markup)
        await state.set_state(AdminStates.approve_ticket_refund)
    else:
        await message.answer('Кажется, такого билета нет в базе!\n\nПопробуйте ввести данные заново!')
        await ticket_refund_start(message, state)


@dp.message(AdminStates.approve_ticket_refund)
async def final_the_refund(message: Message, state: FSMContext):
    data = await state.get_data()
    await api_methods.delete_ticket(ticket_number=data['number_to_refund'],
                                    event=data['event_to_refund'],
                                    ticket_type=data['type_to_refund'])
    field = 'nm_usual' if data['type_to_refund'] == 'Обычный' else 'nm_prime'
    await api_methods.update_ticket_number(event_name=data['event_to_refund'], action='increment', field=field)
    await message.answer('Возврат произошел успешно!')

    ticket_info = await api_methods.get_ticket_by_number_or_type(data['event_to_refund'])

    await update_gdrive(data['event_to_refund'], ticket_info)

    await admin_menu(message, state)
