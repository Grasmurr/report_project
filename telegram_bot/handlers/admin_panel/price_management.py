from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository.api_methods import create_event, get_all_events
from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

from telegram_bot.repository import api_methods