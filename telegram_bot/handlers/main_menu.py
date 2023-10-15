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

# @dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
# async def back_from_upload_data_in_format_final (message: Message, state: FSMContext):
#     await choose_format_for_uploading_data(message, state)
# if message == 'Вернуться в меню администратора':
#         await admin_menu(message, state)


@dp.message(CommandStart())
async def promouter_menu(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.begin_registration)
    markup = create_keyboard_buttons('Зарегистрироваться')
    await message.answer(f'Добро пожаловать в телеграм бот агентства Гамма! '
                         f'Для начала работы необходимо зарегистрироваться в качестве промоутера!',
                         reply_markup=markup)