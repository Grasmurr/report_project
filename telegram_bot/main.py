import logging, sys, asyncio
import aiogram
from telegram_bot.handlers import dp, bot
from telegram_bot.loader import dp, bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


async def start_bot():
    await dp.start_polling(bot)


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())


main()
