from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository.api_methods import create_event, get_all_events
from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

from telegram_bot.repository import api_methods

import datetime


@dp.message(AdminStates.manage_events, F.text == 'Добавить билеты')
async def change_ticket_number(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.enter_event_name_for_ticket_addition)
    await message.answer("Выберите мероприятие для изменения количества билетов:", reply_markup=markup)


@dp.message(AdminStates.enter_event_name)
async def enter_event_name_for_addition(message: Message, state: FSMContext):
    event_name = message.text
    if event_name == 'Назад':
        await admin_menu(message, state)
        return

    events = await api_methods.get_all_events()
    if event_name not in [event['name'] for event in events['data']]:
        await message.answer("Событие не найдено. Попробуйте снова.")
        return

    await state.update_data(event_name=event_name)
    markup = chat_backends.create_keyboard_buttons('Обычные', 'Прайм', 'Назад')
    await state.set_state(AdminStates.enter_ticket_type_to_refund)
    await message.answer("Выберите тип билетов для добавления:", reply_markup=markup)


@dp.message(AdminStates.enter_ticket_type_to_refund)
async def enter_ticket_type_for_addition(message: Message, state: FSMContext):
    ticket_type = message.text
    if ticket_type == 'Назад':
        await state.set_state(AdminStates.manage_events)
        await message.answer("Выберите действие:")
        return

    if ticket_type not in ['Обычные', 'Прайм']:
        await message.answer("Выбран неверный тип билета. Попробуйте снова.")
        return

    await state.update_data(ticket_type=ticket_type)

    if ticket_type == 'Прайм':
        await state.set_state(AdminStates.enter_count_of_event_prime)
    else:
        await state.set_state(AdminStates.enter_count_of_event_normal)

    await message.answer("Введите количество билетов:")


@dp.message(AdminStates.enter_count_of_event_prime)
async def enter_count_of_prime_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_prime=count)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')


@dp.message(AdminStates.enter_count_of_event_normal)
async def enter_count_of_normal_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_usual=count)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')


@dp.message(AdminStates.confirm_event_name)
async def confirm_event_name(message: Message, state: FSMContext):
    if message.text == 'Да':
        event_data = await state.get_data()
        await message.answer("Данные сохранены. Возвращение в главное меню.")
        await state.set_state(AdminStates.main)
    elif message.text == 'Нет':
        await message.answer("Отмена операции. Возвращение в главное меню.")
        await state.set_state(AdminStates.main)
    else:
        await message.answer('Кажется, вы ввели что-то не то. Попробуйте использовать кнопки:')

