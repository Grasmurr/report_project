from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates



from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu


@dp.message(AdminStates.main, F.text == 'Управление мероприятиями')
async def manage_events(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Создать мероприятие', 'Удалить мероприятие', 'Назад')
    await state.set_state(AdminStates.manage_events)
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)


@dp.message(AdminStates.manage_events, F.text == 'Создать мероприятие')
async def create_event(message: Message, state: FSMContext):
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
    await state.update_data(name_of_event=name_of_event)
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
        await message.answer (f'Хорошо. Вы создаете {count_of_prime_tickets} прайм билетов для мероприятия «{data["name_of_event"]}».\n \n'
                              'Теперь введите число обычных билетов, которое вы хотите создать для этого мероприятия:')
        await state.update_data(count_of_prime_tickets=count_of_prime_tickets)
        await state.set_state(AdminStates.enter_count_of_event_normal)
    else:
        await message.answer('Попробуйте ввести количество цифрой. Например: 150')


@dp.message(AdminStates.enter_count_of_event_normal)
async def create_count_of_normal_tickets (message: Message, state: FSMContext):
    if message.text.isdigit():
        count_of_normal_tickets = int(message.text)
        markup = chat_backends.create_keyboard_buttons('Продолжить', 'Ввести данные заново')
        data = await state.get_data()
        count_of_prime_tickets = data['count_of_prime_tickets']
        name_of_event = data['name_of_event']
        await message.answer(f'Хорошо. Вы создаете {count_of_prime_tickets} прайм билетов, '
                             f'а также {count_of_normal_tickets} обычных билетов для мероприятия «{name_of_event}». '
                             f'\n\nЕсли вы передумали, вы можете ввести данные заново',
                             reply_markup=markup)
        await state.update_data(count_of_normal_tickets=count_of_normal_tickets)
        await state.set_state(AdminStates.saving_or_editing_from_the_beginning)
    else:
        await message.answer('Попробуйте ввести количество цифрой. Например: 150')


@dp.message(AdminStates.saving_or_editing_from_the_beginning)
async def success_notification_and_recreate (message: Message, state: FSMContext):
    if message.text == 'Продолжить':
        markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                       "Оформить возврат",
                                                       "Cделать выгрузку данных",
                                                       "Назад")
        await message.answer('Мероприятие было успешно создано!', reply_markup=markup)
        data = await state.get_data()
        for i in data:
            print(f'{i}: {data[i]}')
        # TODO: Эти данные у нас дальше будут ехать в базу, создавая там билеты
        print(data)

        await state.set_state(AdminStates.main)
    else:
        await create_event(message, state)