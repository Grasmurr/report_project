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
from telegram_bot.repository import api_methods

from django.http import HttpResponse, JsonResponse
import re


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
                              'Имя Фамилия \nНомер телефона\nДата рождения в формате ДД:ММ:ГГГГ\nКурс (цифрой)\nЦена билета', reply_markup=ReplyKeyboardRemove())


def check_participant_data(name, phone_number, birth_date, course, ticket_price):
    # Проверка имени и фамилии
    name_pattern = r"^[A-Za-zА-Яа-яЁё]+\s[A-Za-zА-Яа-яЁё]+$"
    if not re.match(name_pattern, name):
        return False

    # Проверка номера телефона
    phone_pattern = r"^\+?[0-9\s()-]+$"
    if not re.match(phone_pattern, phone_number):
        return False

    # Проверка даты рождения
    date_pattern = r"^\d{2}:\d{2}:\d{4}$"
    if not re.match(date_pattern, birth_date):
        return False

    # Проверка курса
    if not course.isdigit():
        return False

    # Проверка цены билета
    if not ticket_price.isdigit() or int(ticket_price) > 10000:
        return False

    return True


@dp.message(PromouterStates.enter_personal_data_of_participant)
async def enter_education_program_of_participant(message: Message, state: FSMContext):
    participant_data = message.text
    data = await state.get_data()
    data_blocks = participant_data.split('\n')
    participant_name = data_blocks[0].split()[0]
    participant_surname = data_blocks[0].split()[1]
    participant_number = data_blocks[1]
    participant_date_of_birth = data_blocks[2]
    participant_course = data_blocks[3]
    participant_ticket_price = data_blocks[4]

    print(participant_name, participant_number, participant_date_of_birth, participant_course, participant_ticket_price)

    # Проверка данных участника
    if not check_participant_data(participant_name, participant_number, participant_date_of_birth, participant_course, participant_ticket_price):
        await message.answer("Неверный формат данных участника. Пожалуйста, повторите ввод.")
        return

    await state.update_data(participant_name=participant_name,
                            participant_surname=participant_surname,
                            participant_number=participant_number,
                            participant_date_of_birth=participant_date_of_birth,
                            participant_course=int(participant_course),
                            participant_ticket_price=int(participant_ticket_price))
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
    participant_name = data['participant_name'],
    participant_surname = data['participant_surname'],
    participant_number = data['participant_number'],
    participant_date_of_birth = data["participant_date_of_birth"],
    participant_course = data['participant_course'],
    participant_ticket_price = data['participant_ticket_price']
    participant_ep = data['participant_ep']
    participant_event = data['participant_event']
    markup = chat_backends.create_keyboard_buttons('Подтвердить', "Изменить тип билета",'Ввести данные участника заново')
    await message.answer(text=f'Подтвердить регистрацию участника на мероприятие "{participant_event}"?\n\n'
                              f'Имя Фамилия : {participant_name} {participant_surname}\n'
                              f'Номер телефона: {participant_number}\n'
                              f'Дата рождения:{participant_date_of_birth}\n'
                              f'Курс: {participant_course}\n'
                              f'Цена билета: {participant_ticket_price}\n'
                              f'Образовательная программа: {participant_ep}\n\n'
                              f'Вид билета: {ticket_type}', reply_markup=markup)
    await state.set_state(PromouterStates.confirm_participant)


@dp.message(PromouterStates.confirm_participant, F.text == "Подтвердить")
async def registration_ends(message: Message, state: FSMContext):
    data = await state.get_data()
    event = await api_methods.get_event(data['participant_event'])

    await api_methods.create_ticket(Event=event,
                                    ticket_number=150,
                                    name=data['participant_name'],
                                    surname=data['participant_surname'],
                                    ticket_type=data['ticket_type'],
                                    date_of_birth=data['participant_date_of_birth'],
                                    price=data['participant_ticket_price'],
                                    educational_program=data['participant_ep'],
                                    educational_course=data['participant_course'])

    markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат")
    await message.answer(text='Спасибо! Участник зарегистрирован', reply_markup=markup)
    await state.set_state(PromouterStates.main_accepted_promouter_panel)


def get_event_by_name(name):
    try:
        event = Event.objects.get(name=name)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    return event


@dp.message(PromouterStates.confirm_participant, F.text == "Изменить тип билета")
async def change_ticket_type(message: Message, state: FSMContext):
    await enter_personal_data_of_participant(message, state)


@dp.message(PromouterStates.confirm_participant, F.text == "Ввести данные участника заново")
async def remake_registration(message: Message, state: FSMContext):
    await enter_ticket_type(message, state)





