
from service.telegram_bot.loader import dp, bot
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
from service.telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
# from aiogram.dispatcher import FSMContext


class MainMenuStates(StatesGroup):
    report_choose = State()


class AdminStates(StatesGroup):
    main = State()
    manage_events = State()
    enter_event_name = State()
    confirm_event_name = State()
    enter_count_of_event_prime = State()
    enter_count_of_event_normal = State()
    saving_or_editing_from_the_beginning = State()


@dp.message(F.text == '/admin')
async def admin_menu(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                   "Оформить возврат",
                                                   "Cделать выгрузку данных",
                                                   "Назад")
    await state.set_state(AdminStates.main)
    await message.answer('Добро пожаловать в админ-панель', reply_markup=markup)


@dp.message(AdminStates.main, F.text == 'Управление мероприятиями')
async def manage_events(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Создать мероприятие', 'Удалить мероприятие', 'Назад')
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)


@dp.message(AdminStates.main, F.text == 'Создать мероприятие')
async def create_event(message: Message, state: FSMContext):
    await message.answer(text='Введите название мероприятия',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdminStates.enter_event_name)


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
        await admin_menu(message=message)
    else:
        await message.answer(text='Хорошо. Теперь введите число прайм билетов, которое вы хотите '
                                  'создать для этого мероприятия:',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AdminStates.enter_count_of_event_prime)


@dp.message(AdminStates.enter_count_of_event_prime)
async def create_count_of_prime_tickets (message: Message, state: FSMContext):
    if message.text.isdigit():
        count_of_prime_tickets = int(message.text)
        data = await state.get_data()
        await message.answer (f'Хорошо. Вы создаете {count_of_prime_tickets} прайм билетов для мероприятия «{data["name_of_event"]}».\n \n'
                              'Теперь введите число обычных билетов, которое вы хотите создать для этого мероприятия:')
        await state.update_data(count_of_prime_tickets=count_of_prime_tickets)
        await state.set_state(AdminStates.enter_count_of_event_normal)
    else:
        await message.answer('Кажется, вы ввели что-то неправильно, попробуйте снова...')


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
        await state.set_state(AdminStates.main)
    else:
        await create_event(message, state)





# НИЖЕ ДАН КОД КОТОРЫЙ БЫЛ ЗДЕСЬ РАНЬШЕ
# class MainMenuStates(StatesGroup):
#     report_choose = State()
#
#
# class AdminStates(StatesGroup):
#     main = State()
#     manage_events = State()
#
#
# @dp.message(CommandStart())
# async def start_message(message: Message):
#     markup = chat_backends.create_keyboard_buttons("Выбрать проект",
#                                                    "Отправить фото",
#                                                    "Создать проект",
#                                                    "Сформировать отчет")
#     await message.answer(text='Добро пожаловать в бот компании "Культура потребления"!',
#                          reply_markup=markup)
#
#
#
#
#
# @dp.message(AdminStates.main, F.text == 'Посмотреть статистику')
# async def choose_project_to_show_statistics(message: Message):
#     markup = chat_backends.create_keyboard_buttons('Фестиваль "К 1 сентября"', 'Столичный марафон', 'Назад')
#     await message.answer(text='Хорошо, выберите для какого проекта вы хотите посмотреть статистику:',
#                          reply_markup=markup)
#
#
# @dp.message(AdminStates.main, F.text == 'Фестиваль "К 1 сентября"')
# async def show_statistics(message: Message):
#     markup = chat_backends.create_keyboard_buttons('Сформировать отчет', 'Отправить рассылку', 'Назад')
#
#     await message.answer(text='Статистика по проекту: Фестиваль "К 1 сентября":\n\n'
#                               'Фотографии загрузили 1 из 2 пользователей\n'
#                               'Кажется, отчет еще не может быть сформирован полноценно. '
#                               'Отправить рассылку пользователям, участвующим в данном проекте?',
#                          reply_markup=markup)
#
#
# @dp.message(AdminStates.main, F.text == 'Отправить рассылку')
# async def send_messages(message: Message):
#     await message.answer('Напоминания были успешно отправлены!')
#
#
# @dp.message(F.text.lower() == 'выбрать проект')
# async def choose_project(message: Message):
#     markup = chat_backends.create_keyboard_buttons('Фестиваль "К 1 сентября"', 'Столичный марафон', 'Назад')
#     await message.answer(text='Хорошо, выберите в какой проект вы хотите загрузить фото:', reply_markup=markup)
#
#
# @dp.message(MainMenuStates.report_choose, F.text.lower().in_(['фестиваль "к 1 сентября"', 'столичный марафон']))
# async def form_report_for_certain_project(message: Message, state: FSMContext):
#     await message.answer(text='Формирую отчет...')
#     await message.answer_document(document=BufferedInputFile(b"hello world", filename='CC__title_sample.pptx'))
#
#
# @dp.message(F.text.lower().in_(['фестиваль "к 1 сентября"', 'столичный марафон']))
# async def festival_example(message: Message):
#     await message.answer(text='Хорошо, загрузите фото:')
#
#
# @dp.message(F.photo)
# async def read_photo(message: Message):
#     await message.answer(text='Хорошо: теперь укажите дату фотографии в формате: 2023-09-30-20:15:15')
#
#
# @dp.message(F.text == 'Сформировать отчет')
# async def form_report(message: Message, state: FSMContext):
#     await state.set_state(MainMenuStates.report_choose)
#     markup = chat_backends.create_keyboard_buttons('Фестиваль "К 1 сентября"', 'Столичный марафон', 'Назад')
#     await message.answer(text='Хорошо, выберите проект, по которому вы хотите сформировать отчет:',
#                          reply_markup=markup)
#
#
# @dp.message(CommandObject)
# async def admin_menu(message: Message, state: FSMContext):
#     markup = chat_backends.create_keyboard_buttons("Посмотреть статистику",
#                                                    "Отправить напоминание",
#                                                    "Создать проект"
#                                                    "Выгрузить отчет",
#                                                    "Вернуться обратно")
#     await state.set_state(AdminStates.main)
#     await message.answer('Добро пожаловать в админ-панель', reply_markup=markup)
#
# @dp.message()
# async def error_message(message: Message):
#     await message.answer('Замечательно! Фото загружено!')
