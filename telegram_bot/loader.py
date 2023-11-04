from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from assets.configs.config import token


bot = Bot(token="5509217734:AAHjjXGtWl_fMMZG5u-JU6wka1MWsigIOkY")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
