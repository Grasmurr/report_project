from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from assets.configs.config import token


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




