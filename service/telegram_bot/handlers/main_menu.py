
from service.telegram_bot.loader import dp, bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import \
    (Message,
     CallbackQuery,
     KeyboardButton,
     ReplyKeyboardMarkup,
     InlineKeyboardMarkup,
     InlineKeyboardButton
     )
from service.telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile

class MainMenuStates(StatesGroup):
    report_choose = State()


class AdminStates(StatesGroup):
    main = State()
    manage_events = State()

@dp.message(F.text == '/admin')
async def admin_menu(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Управление мероприятиями",
                                                   "Оформить возврат",
                                                   "Cделать выгрузку данных",
                                                   "Назад")
    await state.set_state(AdminStates.main)
    await message.answer('Добро пожаловать в админ-панель', reply_markup=markup)



@dp.message(AdminStates.main, F.text == 'Управление мероприятиями')
async def manage_events(message: Message):
    markup = chat_backends.create_keyboard_buttons('Создать мероприятие', 'Удалить мероприятие', 'Назад')
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)

@dp.message(AdminStates.main, F.text == 'Создать мероприятие')
async def create_event(message: Message):
    await message.answer(text='Введите название мероприятия?',
                     reply_markup=markup)

@dp.message(AdminStates.main, F.text == 'Создать мероприятие')
async def create_event(message: Message):
    await message.answer(text='Введите название мероприятия?',
                     reply_markup=markup)

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
