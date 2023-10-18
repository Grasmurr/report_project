from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import PromouterStates

from telegram_bot.handlers.promouter_panel.main_promouter_panel import accepted_promouter_panel
from telegram_bot.repository.api_methods import get_all_events


@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Зарегистрировать участника")
async def choose_event_for_participants_registration(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(PromouterStates.choose_event_for_participants_registration)
    await message.answer(text='Выберите мероприятие, на которое вы хотите зарегистрировать участника',
                         reply_markup=markup)


@dp.message(PromouterStates.choose_event_for_participants_registration, F.text == "Назад")
async def back_from_choose_event_for_participants_registration(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.choose_event_for_participants_registration)
async def enter_personal_data_of_participant(message: Message, state: FSMContext):
    participant_event = message.text
    data = await state.get_data()
    await state.update_data(participant_event=participant_event)
    # непонятно как сохранять мероприятие @рома
    await state.set_state(PromouterStates.enter_personal_data_of_participant)
    await message.answer(text='Введите данные участника в формате:\n\n'
                              'Имя Фамилия \nНомер телефона\nКурс (цифрой)\nЦена билета', reply_markup=ReplyKeyboardRemove())


@dp.message(PromouterStates.enter_personal_data_of_participant)
async def enter_education_program_of_participant(message: Message, state: FSMContext):
    participant_data = message.text
    data = await state.get_data()
    data_blocks = participant_data.split('\n')
    participant_data = {
        'Имя Фамилия': data_blocks[0],
        'Номер телефона': data_blocks[1],
        'Курс': int(data_blocks[2]),
        'Цена билета': int(data_blocks[3])
    }
    await state.update_data(participant_data=participant_data)
    await state.set_state(PromouterStates.enter_education_program_of_participant)
    markup = chat_backends.create_keyboard_buttons('Бизнес информатика', 'Дизайн', 'Маркетинг', 'МиРА', 'МИЭМ',
                                                   'МИЭФ', 'ПАД', 'ПМИ',
                                                   'РиСО', 'Социология', 'УБ', 'ФГН', 'Философия', 'ФКИ', 'ФКН',
                                                   'ФЭН', "Другая ОП", 'Не ВШЭ', 'Назад')
    await message.answer(text='Выберите образовательную программу, на которой обучается участник', reply_markup=markup)


@dp.message(PromouterStates.enter_education_program_of_participant, F.text == 'Назад')
async def back_from_enter_education_program_of_participant(message: Message, state: FSMContext):
    await enter_personal_data_of_participant(message, state)


@dp.message(PromouterStates.enter_education_program_of_participant)
async def enter_ticket_type(message: Message, state: FSMContext):
    participant_ep = message.text
    data = await state.get_data()
    await state.update_data(participant_ep=participant_ep)
    await state.set_state(PromouterStates.enter_ticket_type)
    markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Назад')
    await message.answer(text='Выберите тип билета', reply_markup=markup)


@dp.message(PromouterStates.enter_ticket_type, F.text == 'Назад')
async def back_from_enter_ticket_type(message: Message, state: FSMContext):
    await enter_education_program_of_participant(message, state)


@dp.message(PromouterStates.enter_ticket_type)
async def confirm_participant(message: Message, state: FSMContext):
    ticket_type = message.text
    await state.update_data(ticket_type=ticket_type)
    data = await state.get_data()
    participant_data = data['participant_data']
    participant_ep = data['participant_ep']
    participant_event = data['participant_event']
    markup = chat_backends.create_keyboard_buttons('Подтвердить', "Изменить тип билета",'Ввести данные участника заново')
    await message.answer(text=f'Подтвердить регистрацию участника на мероприятие "{participant_event}"?\n\n'
                              f'Имя Фамилия : {participant_data["Имя Фамилия"]}\n'
                              f'Номер телефона: {participant_data["Номер телефона"]}\n'
                              f'Курс: {participant_data["Курс"]}\n'
                              f'Цена билета: {participant_data["Цена билета"]}\n'
                              f'Образовательная программа: {participant_ep}\n\n'
                              f'Вид билета: {ticket_type}', reply_markup=markup)
    await state.set_state(PromouterStates.confirm_participant)


@dp.message(PromouterStates.confirm_participant, F.text == "Подтвердить")
async def registration_ends(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат")
    await message.answer(text='Спасибо! Участник зарегистрирован', reply_markup=markup)
    await state.set_state(PromouterStates.main_accepted_promouter_panel)


@dp.message(PromouterStates.confirm_participant, F.text == "Изменить тип билета")
async def change_ticket_type(message: Message, state: FSMContext):
    await enter_personal_data_of_participant(message, state)


@dp.message(PromouterStates.confirm_participant, F.text == "Ввести данные участника заново")
async def remake_registration(message: Message, state: FSMContext):
    await enter_ticket_type(message, state)





