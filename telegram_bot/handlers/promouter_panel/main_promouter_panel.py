from telegram_bot.loader import dp, bot
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
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from telegram_bot.states import PromouterStates

from telegram_bot.helpers.chat_backends import create_keyboard_buttons


@dp.message(PromouterStates.begin_registration)
async def identify_promouter(message: Message, state: FSMContext):
    # if message in data:
    await message.answer(f'Хорошо! \n \nДля идентификации, пожалуйста,'
                         f' введите свои имя и фамилию в формате:\nИмя Фамилия',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(PromouterStates.enter_initials)


@dp.message(PromouterStates.enter_initials)
async def identify_promouter_number(message: Message, state: FSMContext):
    if message.text.split() == 2:
        # await message.answer('')

        pass
    else:
        await message.answer('Пожалуйста, введите имя и фамилию в формате "Иван Иванов"')

    if message.isdigit:
        await state.set_state(PromouterStates.main_enter_course)
        markup = chat_backends.create_keyboard_buttons('Бизнес информатика', 'Дизайн', 'Маркетинг', 'МиРА', 'МИЭМ', 'МИЭФ', 'ПАД', 'ПМИ',
                                                                 'РиСО', 'Социология', 'УБ', 'ФГН', 'Философия', 'ФКИ', 'ФКН', 'ФЭН', "Другая ОП", 'Не ВШЭ')

        await message.answer(f'Спасибо! Скажите, на какой образовательной программе вы учитесь?', reply_markup=markup)



