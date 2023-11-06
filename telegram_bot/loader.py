from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from telegram_bot.assets.configs import config

bot = Bot(token=config.token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




