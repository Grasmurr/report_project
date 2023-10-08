import time

import aiogram
from service.telegram_bot.handlers import dp, bot
from service.telegram_bot.loader import dp, bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# @dp.message_handler(commands=['start'])
# def start_message(message: Message):
#     chat_id = get_id(message)
#
#     markup = create_keyboard_buttons("Выбрать проект", "Отправить фото", "Создать проект", "Сформировать отчет")
#
#     bot.send_message(chat_id=chat_id, text='Добро пожаловать в бот компании "Культура потребления"!',
#                      reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Выбрать проект')
# def info_message(message: Message):
#     chat_id = get_id(message)
#
#     markup =create_keyboard_buttons('Фестиваль "К 1 сентября"', 'Столичный марафон', 'Назад')
#
#     bot.send_message(chat_id=chat_id, text='Выберите проект, в который вы хотите загрузить фото', reply_markup=markup)
#
#
#
# @bot.message_handler(content_types=['text'])
# def error(message: Message):
#     chat_id = get_id(message)
#     bot.send_message(chat_id=chat_id, text='Вы ввели неправильный пин код!')
#
#
# @bot.callback_query_handler(func=lambda call: call.data == '1')
# def info_subbotton(call: CallbackQuery):
#     chat_id = call.from_user.id
#
#     bot.send_message(chat_id, 'ПРИПРИВЕТ!!!')
#     bot.edit_message_text()
#
# from aiogram.filters import CommandStart
# from service.telegram_bot.helpers import chat_backends
#
# @dp.message(CommandStart())
# async def start_message(message: Message):
#     chat_id = chat_backends.get_id_from_message(message)
#
#     markup = chat_backends.create_keyboard_buttons("Выбрать проект", "Отправить фото", "Создать проект", "Сформировать отчет")
#
#     await bot.send_message(chat_id=chat_id, text='Добро пожаловать в бот компании "Культура потребления"!',
#                      reply_markup=markup)


async def start_bot():
    await dp.start_polling(bot)

# 10000 раз в секунду - есть что-то от тебя?

# да, привет



