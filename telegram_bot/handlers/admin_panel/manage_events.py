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

from telegram_bot.gdrive import api_methods

import datetime


@dp.message(AdminStates.main, F.text == 'Управление мероприятиями')
async def manage_events(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Создать мероприятие',
                                                   'Добавить билеты',
                                                   'Изменить ценовой диапазон',
                                                   'Скрыть/показать мероприятие',
                                                   'Назад')
    await state.set_state(AdminStates.manage_events)
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)


@dp.message(AdminStates.manage_events, F.text == 'Создать мероприятие')
async def create_new_event(message: Message, state: FSMContext):
    await message.answer(text='Введите название мероприятия',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdminStates.enter_event_name)


@dp.message(AdminStates.manage_events, F.text == 'Удалить мероприятие')
async def delete_event(message: Message, state: FSMContext):
    await message.answer(text='Выберите мероприятие, которое вы хотите удалить:',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdminStates.delete_event)


@dp.message(AdminStates.manage_events, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.enter_event_name)
async def enter_event_name(message: Message, state: FSMContext):
    name_of_event = message.text
    markup = chat_backends.create_keyboard_buttons('Да', 'Назад')
    await message.answer(f'Вы хотите создать мероприятие «{name_of_event}». Продолжить?',
                         reply_markup=markup)
    await state.update_data(name=name_of_event)
    await state.set_state(AdminStates.confirm_event_name)


@dp.message(AdminStates.confirm_event_name)
async def question_continue_create_event(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await manage_events(message, state)
    else:
        await message.answer(text='Хорошо. Теперь введите число прайм билетов, которое вы хотите '
                                  'создать для этого мероприятия:',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AdminStates.enter_count_of_event_prime)


@dp.message(AdminStates.enter_count_of_event_prime)
async def create_count_of_prime_tickets(message: Message, state: FSMContext):
    if message.text.isdigit():
        count_of_prime_tickets = int(message.text)
        data = await state.get_data()
        await message.answer(f'Хорошо. Вы создаете {count_of_prime_tickets} прайм билетов для мероприятия «{data["name"]}».\n\n'
                              'Теперь введите число обычных билетов, которое вы хотите создать для этого мероприятия:')
        await state.update_data(nm_prime=count_of_prime_tickets)
        await state.set_state(AdminStates.enter_count_of_event_normal)
    else:
        await message.answer('Попробуйте ввести количество цифрой. Например: 150')


@dp.message(AdminStates.enter_count_of_event_normal)
async def create_count_of_normal_tickets (message: Message, state: FSMContext):
    if message.text.isdigit():
        count_of_normal_tickets = int(message.text)
        data = await state.get_data()
        count_of_prime_tickets = data['nm_prime']
        name_of_event = data['name']
        await message.answer(f'Хорошо. Вы создаете {count_of_prime_tickets} прайм билетов, '
                             f'а также {count_of_normal_tickets} обычных билетов для мероприятия «{name_of_event}». '
                             f'\n\nПожалуйста, введите дату в '
                             f'формате YYYY-MM-DD. Например: 2023-10-29')
        await state.update_data(nm_usual=count_of_normal_tickets)
        await state.set_state(AdminStates.enter_event_date)
    else:
        await message.answer('Попробуйте ввести количество цифрой. Например: 150')


@dp.message(AdminStates.enter_event_date)
async def create_event_date(message: Message, state: FSMContext):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        event_date_str = event_date.strftime('%Y-%m-%d')
        await state.update_data(event_date=event_date_str)

        await message.answer(f'Дата мероприятия установлена на {event_date_str}\n\nА теперь, введите список цен, которое вы хотите предусмотреть:'
                             '\n\nНапример:\n1500\n2000\n2500\n\nКаждое с новой строки!')
        await state.set_state(AdminStates.enter_prices_range)

    except ValueError:
        await message.answer('Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29')


@dp.message(AdminStates.enter_prices_range)
async def handle_prices_range(message: Message, state: FSMContext):
    rng = message.text.split('\n')
    print(rng)
    if not rng:
        await message.answer('Попробуйте ввести список еще раз')
    try:
        rng = [int(i) for i in rng]
        print(rng)
        await state.update_data(prices_range=rng)
        data = await state.get_data()
        str_prices = [str(i) for i in data["prices_range"]]
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Ввести данные заново')
        await message.answer(f'Хорошо! Вы добавляете мероприятие {data["name"]}\n'
                             f'Количество билетов:\nОбычных:{data["nm_usual"]}\nПрайм:{data["nm_prime"]}\n\n'
                             f'Дата:{data["event_date"]}\n\nЦеновой диапазон: {"-".join(str_prices)}', reply_markup=buttons)
        await state.set_state(AdminStates.saving_or_editing_from_the_beginning)
    except:
        await message.answer('Попробуйте ввести список еще раз')


@dp.message(AdminStates.saving_or_editing_from_the_beginning)
async def success_notification_and_recreate(message: Message, state: FSMContext):
    if message.text == 'Продолжить':
        markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                       "Оформить возврат",
                                                       "Cделать выгрузку данных",
                                                       "Назад")
        await message.answer('Мероприятие было успешно создано!', reply_markup=markup)
        data = await state.get_data()
        for i in data:
            print(f'{i}: {data[i]}')
        print(data)
        # TODO: добавить в дату nm_deposit для засылки в базу
        await create_event(name=data['name'],
                           nm_prime=data['nm_prime'],
                           nm_usual=data['nm_usual'],
                           nm_deposit=data['nm_deposit'],
                           event_date=data['event_date'],
                           prices=data['prices_range'])
        api_methods.create_sheet(data['name'])

        events = await get_all_events()
        await message.answer(text=f'Вы успешно создали мероприятие: {events}')
        await state.set_state(AdminStates.main)
    else:
        await create_new_event(message, state)
