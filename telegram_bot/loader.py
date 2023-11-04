from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from assets.configs.config import token


bot = Bot(token="6529076927:AAF3IIlMbvk2nDIZvxPpH9Kt0N8c-lbTI3w")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)




