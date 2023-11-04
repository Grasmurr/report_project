from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository import api_methods


@dp.message(F.text == 'Рассылка')
async def start_mailing(message: Message, state: FSMContext):
    pass

