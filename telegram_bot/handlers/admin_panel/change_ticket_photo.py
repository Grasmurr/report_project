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

import datetime, os


@dp.message(AdminStates.manage_events, F.text == 'Изменить фотографию билета')
async def change_ticket_photo(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.enter_event_name_for_ticket_photo)
    await message.answer("Выберите мероприятие, для которого "
                         "вы хотите загрузить новый макет билета:", reply_markup=markup)


@dp.message(AdminStates.enter_event_name_for_ticket_photo)
async def enter_event_name_for_ticket_photo(message: Message, state: FSMContext):
    event_name = message.text
    if event_name == 'Назад':
        await admin_menu(message, state)
        return

    events = await api_methods.get_all_events()
    if event_name not in [event['name'] for event in events['data']]:
        await message.answer("Событие не найдено. Попробуйте снова.")
        return

    await state.update_data(event_name=event_name)
    markup = chat_backends.create_keyboard_buttons('Обычный', 'Bundle', 'Депозит', 'Прайм', 'Назад')
    await message.answer("Пожалуйста, выберите тип билета, для которого вы хотите поставить новую фотографию",
                         reply_markup=markup)
    await state.set_state(AdminStates.catching_new_photo_type_choice)


@dp.message(AdminStates.catching_new_photo_type_choice, F.text == 'Назад')
async def catching_new_photo_back(message: Message, state: FSMContext):
    await change_ticket_photo(message, state)


@dp.message(AdminStates.catching_new_photo_type_choice)
async def catching_new_photo_type_choose(message: Message, state: FSMContext):
    ticket_type = message.text
    if ticket_type not in ['Обычный', 'Bundle', 'Депозит', 'Прайм']:
        markup = chat_backends.create_keyboard_buttons('Обычный', 'Bundle', 'Депозит', 'Прайм', 'Назад')
        await message.answer('Кажется, вы нажали не туда. Пожалуйста, воспользуйтесь кнопками', reply_markup=markup)
        return
    await state.update_data(ticket_type=ticket_type)
    await message.answer(f'Хорошо! Загрузите новую фотографию для билетов типа {ticket_type}')
    await state.set_state(AdminStates.catching_new_photo)


@dp.message(AdminStates.catching_new_photo, F.photo)
async def catching_new_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id

    save_path = '/usr/src/telegram_bot/handlers/promouter_panel/assets/'
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %I.%M.%S %p")
    file_name = f'{current_time}.jpg'
    full_path = os.path.join(save_path, file_name)

    file_path = await bot.get_file(file_id)
    await bot.download_file(file_path.file_path, destination=full_path)

    data = await state.get_data()

    ticket_type = data['ticket_type']

    if ticket_type == 'Обычный':
        await api_methods.update_event_data(name=data['event_name'],
                                            ticket_path_usual=full_path,
                                            photo_id_usual=file_id)
    elif ticket_type == 'Bundle':
        await api_methods.update_event_data(name=data['event_name'],
                                            ticket_path_bundle=full_path,
                                            photo_id_bundle=file_id)
    elif ticket_type == 'Депозит':
        await api_methods.update_event_data(name=data['event_name'],
                                            ticket_path_deposit=full_path,
                                            photo_id_deposit=file_id)
    else:
        await api_methods.update_event_data(name=data['event_name'],
                                            ticket_path_prime=full_path,
                                            photo_id_prime=file_id)

    await message.answer("Фотография билета успешно обновлена!")
    await state.clear()
    await admin_menu(message, state)


@dp.message(AdminStates.catching_new_photo, F.text)
async def back_from_enter_event_name_for_ticket_photo(message: Message, state: FSMContext):
    if message.text == "Назад":
        await change_ticket_photo(message, state)
    else:
        await message.answer("Кажется, вы нажали не туда. Возвращаем вас в админ-панель!")
        await state.clear()
        await admin_menu(message, state)
