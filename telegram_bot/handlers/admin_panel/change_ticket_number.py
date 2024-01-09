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


@dp.message(AdminStates.enter_event_name_for_ticket_addition)
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
    markup = chat_backends.create_keyboard_buttons('Обычные', 'Bundle', 'Депозит', 'Прайм', 'Назад')
    await state.set_state(AdminStates.enter_ticket_type_for_addition)
    await message.answer("Выберите тип билетов для изменения:", reply_markup=markup)


@dp.message(AdminStates.enter_ticket_type_for_addition)
async def enter_ticket_type_for_addition(message: Message, state: FSMContext):
    ticket_type = message.text
    if ticket_type == 'Назад':
        await state.set_state(AdminStates.manage_events)
        await message.answer("Выберите действие:")
        return

    if ticket_type not in ['Обычные', 'Bundle', 'Прайм', 'Депозит']:
        await message.answer("Выбран неверный тип билета. Попробуйте снова.")
        return

    await state.update_data(ticket_type=ticket_type)

    if ticket_type == 'Прайм':
        await state.set_state(AdminStates.enter_count_of_event_prime_for_addition)
    elif ticket_type == 'Обычные':
        await state.set_state(AdminStates.enter_count_of_event_normal_for_addition)
    elif ticket_type == 'Bundle':
        await state.set_state(AdminStates.enter_count_of_event_bundle_for_addition)
    else:
        await state.set_state(AdminStates.enter_count_of_event_deposit_for_addition)

    await message.answer("Введите количество билетов:", reply_markup=ReplyKeyboardRemove())


@dp.message(AdminStates.enter_count_of_event_normal_for_addition)
async def enter_count_of_prime_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_usual=count)
        data = await state.get_data()
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Начать заново')
        await message.answer(f'Хорошо! Вы хотите установить колмчество {count} обычных билетов для мероприятия '
                             f'{data["event_name"]}. '
                             f'\n\nПродолжить?', reply_markup=buttons)
        await state.set_state(AdminStates.confirm_event_addition_tickets)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')


@dp.message(AdminStates.enter_count_of_event_bundle_for_addition)
async def enter_count_of_normal_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_bundle=count)
        data = await state.get_data()
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Начать заново')
        await message.answer(f'Хорошо! Вы хотите установить количество {count} bundle билетов для мероприятия '
                             f'{data["event_name"]}.'
                             f'\n\nПродолжить?', reply_markup=buttons)
        await state.set_state(AdminStates.confirm_event_addition_tickets)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')



@dp.message(AdminStates.enter_count_of_event_prime_for_addition)
async def enter_count_of_normal_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_prime=count)
        data = await state.get_data()
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Начать заново')
        await message.answer(f'Хорошо! Вы хотите установить количество {count} прайм билетов для мероприятия '
                             f'{data["event_name"]}.'
                             f'\n\nПродолжить?', reply_markup=buttons)
        await state.set_state(AdminStates.confirm_event_addition_tickets)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')


@dp.message(AdminStates.enter_count_of_event_deposit_for_addition)
async def enter_count_of_deposit_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count = int(message.text)
        await state.update_data(nm_deposit=count)
        data = await state.get_data()
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Начать заново')
        await message.answer(f'Хорошо! Вы хотите установить количество {count} депозитных билетов для мероприятия '
                             f'{data["event_name"]}.'
                             f'\n\nПродолжить?', reply_markup=buttons)
        await state.set_state(AdminStates.confirm_event_addition_tickets)
    else:
        await message.answer('Кажется, вы ввели число в неправильном формате! Попробуйте написать вот так: 150')


@dp.message(AdminStates.confirm_event_addition_tickets)
async def confirm_event_name(message: Message, state: FSMContext):
    if message.text == 'Продолжить':
        event_data = await state.get_data()
        print(event_data)
        if "nm_usual" in event_data:
            type = 'обычных'
            count = event_data['nm_usual']
            await api_methods.update_event_data(name=event_data['event_name'], nm_usual=count)
        elif "nm_deposit" in event_data:
            type = 'депозитных'
            count = event_data['nm_deposit']
            await api_methods.update_event_data(name=event_data['event_name'], nm_deposit=count)
        elif "nm_bundle" in event_data:
            type = 'bundle'
            count = event_data['nm_bundle']
            await api_methods.update_event_data(name=event_data['event_name'], nm_bundle=count)
        else:
            type = 'прайм'
            count = event_data['nm_prime']
            await api_methods.update_event_data(name=event_data['event_name'], nm_prime=count)

        await message.answer(f"Хорошо! Вы установили количество {count} {type} билетов для мероприятия "
                             f"{event_data['event_name']}")
        await state.clear()
        await admin_menu(message, state)
    elif message.text == 'Начать заново':
        await message.answer("Отмена операции.")
        await change_ticket_number(message, state)
    else:
        await message.answer('Кажется, вы ввели что-то не то. Попробуйте использовать кнопки:')

