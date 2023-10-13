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
from service.telegram_bot.states import AdminStates









# @dp.message(AdminStates.upload_data_in_format_final, F.text == 'Выгрузить в другом формате')
# async def back_from_upload_data_in_format_final (message: Message, state: FSMContext):
#     await choose_format_for_uploading_data(message, state)
# if message == 'Вернуться в меню администратора':
#         await admin_menu(message, state)
