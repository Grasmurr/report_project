import random, re, tempfile, os

from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

from telegram_bot.states import PromouterStates
from telegram_bot.handlers.promouter_panel.main_promouter_panel import accepted_promouter_panel
from telegram_bot.repository.api_methods import get_all_events, get_promouter
from telegram_bot.repository import api_methods

from telegram_bot.assets.configs import config

from telegram_bot.gdrive.api_methods import update_gdrive

from PIL import Image, ImageFont, ImageDraw


@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Зарегистрировать участника")
async def choose_event_for_participants_registration(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(PromouterStates.choose_event_for_participants_registration)
    await message.answer(text='Выберите мероприятие, на которое вы хотите зарегистрировать участника',
                         reply_markup=markup)


@dp.message(PromouterStates.choose_event_for_participants_registration, F.text == "Назад")
async def back_from_choose_event_for_participants_registration(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.choose_event_for_participants_registration)
async def enter_personal_data_of_participant(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    if message.text not in event_names and message.text != "Назад" and message.text != "Ввести данные участника заново":
        await message.answer(text='Кажется такого мероприятия не существует! Попробуйте выбрать '
                                  'название мероприятия из представленных на кнопках ниже')
        return
    if message.text != "Назад" and message.text != "Ввести данные участника заново":
        participant_event = message.text
    else:
        data = await state.get_data()
        participant_event = data["participant_event"]
    data = await state.get_data()
    await state.update_data(participant_event=participant_event)
    await state.set_state(PromouterStates.enter_personal_data_of_participant)
    buttons = chat_backends.create_keyboard_buttons('Назад')
    await message.answer(text='Введите данные участника в формате:\n\n'
                              'Имя Фамилия \nНомер телефона\nДата рождения в формате ДД.ММ.ГГГГ'
                              '\nКурс (цифрой)', reply_markup=buttons)


@dp.message(PromouterStates.enter_personal_data_of_participant, F.text == 'Назад')
async def enter_sex_of_participant(message: Message, state: FSMContext):
    await choose_event_for_participants_registration(message, state)


def check_participant_data(name, surname, phone_number, birth_date, course):
    # Проверка имени и фамилии
    if not name.isalpha():
        return False

    if not surname.isalpha():
        return False

    phone_number = ''.join([i for i in phone_number if i.isdigit()])
    if not phone_number.isdigit() or len(phone_number) != 11:
        return False

    date_pattern = r"^\d{2}.\d{2}.\d{4}$"
    if not re.match(date_pattern, birth_date):
        return False

    # Проверка курса
    if not course.isdigit():
        return False

    # if not ticket_price.isdigit() or int(ticket_price) > 10000:
    #     return False

    return True


@dp.message(PromouterStates.enter_personal_data_of_participant)
async def enter_sex_of_participant(message: Message, state: FSMContext):
    participant_data = message.text
    data = await state.get_data()
    data_blocks = participant_data.split('\n')
    if message.text != "Назад" and message.text != "Ввести данные участника заново":
        if len(data_blocks) != 4 or len(data_blocks[0].split()) != 2:
            await message.answer('Кажется, вы ввели данные об участнике в неверном формате! '
                                 'Обратите внимание на форму выше!')
            return
    print(data_blocks[0])
    participant_name = data_blocks[0].split()[0]
    print(participant_name)
    participant_surname = data_blocks[0].split()[1]
    participant_number = data_blocks[1]
    participant_date_of_birth = data_blocks[2]
    participant_course = data_blocks[3]
    # participant_ticket_price = data_blocks[4]

    print(participant_name, participant_number, participant_date_of_birth, participant_course)

    if not check_participant_data(name=participant_name,
                                  surname=participant_surname,
                                  phone_number=participant_number,
                                  birth_date=participant_date_of_birth,
                                  course=participant_course):
        await message.answer("Кажется, вы ввели данные об участнике в неверном формате! "
                             "Обратите внимание на форму выше!")
        return

    await state.update_data(participant_name=participant_name,
                            participant_surname=participant_surname,
                            participant_number=participant_number,
                            participant_date_of_birth=participant_date_of_birth,
                            participant_course=int(participant_course),
                            participant_phone_number=participant_number)
    await state.set_state(PromouterStates.enter_participant_gender)
    markup = chat_backends.create_keyboard_buttons("Мужской", "Женский", "Назад")
    await message.answer(text='Укажите пол участника', reply_markup=markup)


@dp.message(PromouterStates.enter_participant_gender, F.text == 'Назад')
async def back_from_enter_education_program_of_participant(message: Message, state: FSMContext):
    await enter_personal_data_of_participant(message, state)


@dp.message(PromouterStates.enter_participant_gender, F.text.in_(["Мужской", "Женский"]))
async def enter_education_program_of_participant(message: Message, state: FSMContext):
    ticket_holder_sex = message.text
    await state.update_data(participant_gender=ticket_holder_sex)
    await state.set_state(PromouterStates.enter_education_program_of_participant)
    markup = chat_backends.create_keyboard_buttons('Бизнес информатика', 'Дизайн', 'Маркетинг', 'МиРА', 'МИЭМ',
                                                   'МИЭФ', 'ПАД', 'ПМИ',
                                                   'РиСО', 'Социология', 'УБ', 'ФГН', 'Философия', 'ФКИ', 'ФКН',
                                                   'ФЭН', "Другая ОП", 'Не ВШЭ', 'Назад')
    await message.answer(text='Выберите образовательную программу, на которой обучается участник', reply_markup=markup)


@dp.message(PromouterStates.enter_education_program_of_participant, F.text == 'Назад')
async def back_from_enter_education_program_of_participant(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.enter_participant_gender)
    markup = chat_backends.create_keyboard_buttons("Мужской", "Женский", "Назад")
    await message.answer(text='Укажите пол участника', reply_markup=markup)


@dp.message(PromouterStates.enter_education_program_of_participant)
async def enter_ticket_type(message: Message, state: FSMContext):
    ep_list = ['Бизнес информатика', 'Дизайн', 'Маркетинг', 'МиРА',
               'МИЭМ', 'МИЭФ', 'ПАД', 'ПМИ', 'РиСО', 'Социология',
               'УБ', 'ФГН', 'Философия', 'ФКИ', 'ФКН', 'ФЭН', "Другая ОП",
               'Не ВШЭ']
    if message.text not in ep_list and message.text != "Изменить тип билета" and  message.text != "Назад":
        await message.answer('Кажется вы ввели название образовательной программы с '
                             'клавиатуры. Пожалуйста, используйте кнопки')
        return

    if message.text == "Изменить тип билета" or message.text == "Назад":
        data = await state.get_data()
        participant_ep = data['participant_ep']
    else:
        participant_ep = message.text

    data = await state.get_data()
    event = data['participant_event']
    print(event)
    await state.update_data(participant_ep=participant_ep)
    event_data = await api_methods.get_event_by_name(event)

    nm_prime = event_data['data'][0]['nm_prime']
    nm_usual = event_data['data'][0]['nm_usual']
    nm_deposit = event_data['data'][0]['nm_deposit']

    markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Депозит', 'Назад')
    await message.answer(
        text=f'Выберите тип билета:\n\nОбычный (Осталось {nm_usual})\nПрайм (Осталось {nm_prime})\nДепозит (Осталось'
             f' {nm_deposit})',
        reply_markup=markup)
    await state.set_state(PromouterStates.enter_ticket_type)


@dp.message(PromouterStates.enter_ticket_type, F.text == 'Назад')
async def back_from_enter_ticket_type(message: Message, state: FSMContext):
    await enter_education_program_of_participant(message, state)


@dp.message(PromouterStates.enter_ticket_type)
async def confirm_participant(message: Message, state: FSMContext):
    ticket_type = message.text
    if ticket_type != 'Обычный' and ticket_type != 'Прайм' and ticket_type != 'Депозит':
        await message.answer("Кажется, вы нажали не туда! Пожалуйста используйте "
                             "кнопки ниже чтобы выбрать тип билета")

    await state.update_data(ticket_type=ticket_type)
    data = await state.get_data()
    print(data)
    event = data['participant_event']
    event_data = await api_methods.get_event_by_name(event)
    nm_prime = event_data['data'][0]['nm_prime']
    nm_usual = event_data['data'][0]['nm_usual']
    nm_deposit = event_data['data'][0]['nm_deposit']
    if (ticket_type == 'Прайм' and nm_prime <= 0) or (ticket_type == 'Обычный' and nm_usual <= 0) or (
            ticket_type == 'Депозит' and nm_deposit <= 0):
        markup = chat_backends.create_keyboard_buttons(f'Обычный', f'Прайм',
                                                       f'Депозит', 'Назад')
        await message.answer(
            text=f'Извините, билеты типа {ticket_type} закончились. Пожалуйста, выберите другой тип билета:\n\n'
                 f'Обычный (Осталось {nm_usual})\nПрайм (Осталось {nm_prime})\nДепозит (Осталось'
             f' {nm_deposit})',
            reply_markup=markup)
        await state.set_state(PromouterStates.enter_ticket_type)
        return

    prices = event_data['data'][0]["prices"]
    print(prices)
    prices = [str(num) for num in prices]
    markup = chat_backends.create_keyboard_buttons(*prices, 'Назад')

    await message.answer("Выберите цену, по которой был продан билет",
                         reply_markup=markup)
    await state.set_state(PromouterStates.enter_price)


@dp.message(PromouterStates.enter_price, F.text == 'Назад')
async def back_from_choose_price_for_ticket(message: Message, state: FSMContext):
    await enter_ticket_type(message, state)


@dp.message(PromouterStates.enter_price)
async def confirm_participant(message: Message, state: FSMContext):
    data = await state.get_data()
    event = data['participant_event']
    event_data = await api_methods.get_event_by_name(event)
    prices = event_data['data'][0]["prices"]
    prices = [str(num) for num in prices]

    ticket_type = data['ticket_type']
    nm_prime = event_data['data'][0]['nm_prime']
    nm_usual = event_data['data'][0]['nm_usual']
    nm_deposit = event_data['data'][0]['nm_deposit']
    if (ticket_type == 'Прайм' and nm_prime <= 0) or (ticket_type == 'Обычный' and nm_usual <= 0) or (
            ticket_type == 'Депозит' and nm_deposit <= 0):
        markup = chat_backends.create_keyboard_buttons(f'Обычный', f'Прайм',
                                                       f'Депозит', 'Назад')
        await message.answer(
            text=f'Извините, билеты типа {ticket_type} закончились. Пожалуйста, выберите другой тип билета:\n\n'
                 f'Обычный (Осталось {nm_usual})\nПрайм (Осталось {nm_prime})\nДепозит (Осталось'
             f' {nm_deposit})',
            reply_markup=markup)
        await state.set_state(PromouterStates.enter_ticket_type)
        return

    if message.text not in prices:
        await message.answer(text="Пожалуйста, выберите цену из предложенных на кнопках")
        return
    participant_ticket_price = message.text
    await state.update_data(participant_ticket_price=participant_ticket_price)

    await state.get_data()
    print(data)
    participant_name = data['participant_name']
    participant_surname = data['participant_surname']
    participant_gender = data['participant_gender']
    participant_number = data['participant_number']
    participant_date_of_birth = data["participant_date_of_birth"]
    participant_course = data['participant_course']
    participant_ticket_price = participant_ticket_price
    participant_ep = data['participant_ep']
    participant_event = data['participant_event']
    ticket_type = data['ticket_type']

    markup = chat_backends.create_keyboard_buttons('Подтвердить', "Отменить регистрацию этого билета",
                                                   "Изменить тип билета", 'Ввести данные участника заново')
    await message.answer(text=f'Подтвердить регистрацию участника на мероприятие "{participant_event}"?\n\n'
                              f'Имя Фамилия : {participant_name} {participant_surname}\n'
                              f'Пол: {participant_gender}\n'
                              f'Номер телефона: {participant_number}\n'
                              f'Дата рождения: {participant_date_of_birth}\n'
                              f'Курс: {participant_course}\n'
                              f'Образовательная программа: {participant_ep}\n\n'
                              f'Вид билета: {ticket_type}\n'
                              f'Цена билета: {participant_ticket_price}', reply_markup=markup)
    await state.set_state(PromouterStates.confirm_participant)


# TODO: Что делать с дизайном билетов?
async def create_image(text, photo_path):

    with open(photo_path, 'rb') as file:
        image = Image.open(file).copy()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/src/telegram_bot/handlers/promouter_panel/assets/arial.ttf", 100)
    position = (950, 380)
    color = "black"
    draw.text(position, str(text), color, font=font)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    image.save(temp_file, format='JPEG')
    temp_file_path = temp_file.name
    temp_file.close()
    return temp_file_path


@dp.message(PromouterStates.confirm_participant, F.text == "Подтвердить")
async def registration_ends(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_type = data['ticket_type']
    event = data['participant_event']
    event_data = await api_methods.get_event_by_name(event)
    nm_prime = event_data['data'][0]['nm_prime']
    nm_usual = event_data['data'][0]['nm_usual']
    nm_deposit = event_data['data'][0]['nm_deposit']
    if (ticket_type == 'Прайм' and nm_prime <= 0) or (ticket_type == 'Обычный' and nm_usual <= 0) or (
            ticket_type == 'Депозит' and nm_deposit <= 0):
        markup = chat_backends.create_keyboard_buttons(f'Обычный', f'Прайм',
                                                       f'Депозит', 'Назад')
        await message.answer(
            text=f'Извините, билеты типа {ticket_type} закончились. Пожалуйста, выберите другой тип билета:\n\n'
                 f'Обычный (Осталось {nm_usual})\nПрайм (Осталось {nm_prime})\nДепозит (Осталось'
             f' {nm_deposit})',
            reply_markup=markup)
        await state.set_state(PromouterStates.enter_ticket_type)
        return

    data = await state.get_data()

    num = await chat_backends.generate_next_ticket_number(event_name=data['participant_event'],
                                                          ticket_type=data['ticket_type'])

    temp_file_path = await create_image(num, event_data['data'][0]['ticket_path'])

    with open(temp_file_path, 'rb') as file:
        await message.answer_photo(photo=BufferedInputFile(file.read(), filename='file.jpg*'))

    count_of_ticket_to_check = await api_methods.get_event_by_name(data['participant_event'])

    nm_prime_before_change = count_of_ticket_to_check['data'][0]['nm_prime']
    nm_usual_before_change = count_of_ticket_to_check['data'][0]['nm_usual']
    nm_deposit_before_change = count_of_ticket_to_check['data'][0]['nm_deposit']

    field = 'nm_usual' if data['ticket_type'] == 'Обычный' else 'nm_prime' \
        if data['ticket_type'] == 'Прайм' else 'nm_deposit'
    await api_methods.update_ticket_number(event_name=data['participant_event'], action='decrement', field=field)

    count_of_ticket_to_check = await api_methods.get_event_by_name(data['participant_event'])
    print(count_of_ticket_to_check)

    nm_prime_to_check = count_of_ticket_to_check['data'][0]['nm_prime']
    nm_usual_to_check = count_of_ticket_to_check['data'][0]['nm_usual']
    nm_deposit_to_check = count_of_ticket_to_check['data'][0]['nm_deposit']

    user_id = message.from_user.id

    if (nm_prime_to_check <= 0 and nm_prime_to_check != nm_prime_before_change) or \
            (nm_usual_to_check <= 0 and nm_usual_before_change != nm_usual_to_check) or \
            (nm_deposit_to_check <= 0 and nm_deposit_before_change != nm_deposit_to_check):
        await bot.send_message(chat_id=config.ADMIN_ID,
                               text=f'Возможно, вы хотите довыпустить билеты для мероприятия '
                                    f'«{data["participant_event"]}»\n\n'
                                    f'На данный момент в наличии:\n'
                                    f'Прайм: {nm_prime_to_check}\n'
                                    f'Обычных: {nm_usual_to_check}\n'
                                    f'Депозитных: {nm_deposit_to_check}\n\n'
                                    f'Для дополнительной эмиссии билетов перейдите в раздел '
                                    f'«Управление мероприятиями» → «Добавить билеты»')

    print(user_id)

    promouter = await api_methods.get_promouter(user_id)
    name = promouter['data'][0]['full_name']

    await api_methods.create_ticket(event=data['participant_event'],
                                    ticket_number=num,
                                    name=data['participant_name'],
                                    surname=data['participant_surname'],
                                    gender=data['participant_gender'],
                                    ticket_type=data['ticket_type'],
                                    date_of_birth=data['participant_date_of_birth'],
                                    price=data['participant_ticket_price'],
                                    educational_program=data['participant_ep'],
                                    educational_course=data['participant_course'],
                                    phone_number=data['participant_phone_number'],
                                    promouter_name=name)

    await message.answer(text='Спасибо! Участник зарегистрирован')
    await accepted_promouter_panel(message, state)
    ticket_info = await api_methods.get_ticket_by_number_or_type(data['participant_event'])
    await update_gdrive(data['participant_event'], ticket_info)


@dp.message(PromouterStates.confirm_participant, F.text == "Отменить регистрацию этого билета")
async def cancel_participant_regintration(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.confirm_participant, F.text == "Изменить тип билета")
async def change_ticket_type(message: Message, state: FSMContext):
    await enter_ticket_type(message, state)


@dp.message(PromouterStates.confirm_participant, F.text == "Ввести данные участника заново")
async def remake_registration(message: Message, state: FSMContext):
    await enter_personal_data_of_participant(message, state)
