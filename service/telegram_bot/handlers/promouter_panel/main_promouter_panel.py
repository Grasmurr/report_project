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
from service.telegram_bot.states import PromouterStates

@dp.message(F.text == '/promouter')
async def promouter_menu(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.main)
    await message.answer(f'Добро пожаловать в промоутер-панель. \n \nДля идентификации, пожалуйста, введите свои имя и фамилию в формате:\nИмя Фамилия', reply_markup = ReplyKeyboardRemove())


@dp.message(PromouterStates.main)
async def identify_promouter(message: Message, state: FSMContext):
    # if message in data:
    await state.set_state(PromouterStates.main_enter_telephone)
    await message.answer(f'Добрый день {message.text}!\n\nТеперь, пожалуйста, введите номер телефона')

@dp.message(PromouterStates.main_enter_telephone)
async def identify_promouter_number(message: Message, state: FSMContext):
    if message.isdigit:
        await state.set_state(PromouterStates.main_enter_course)
        markup = chat_backends.create_keyboard_buttons('Бизнес информатика','Дизайн', 'Маркетинг', 'МиРА', 'МИЭМ', 'МИЭФ', 'ПАД', 'ПМИ',
                                                                 'РиСО', 'Социология', 'УБ', 'ФГН', 'Философия', 'ФКИ', 'ФКН', 'ФЭН', "Другая ОП", 'Не ВШЭ')

        await message.answer(f'Спасибо! Скажите, на какой образовательной программе вы учитесь?', reply_markup=markup)



