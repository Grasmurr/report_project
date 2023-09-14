import time

import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

bot = telebot.TeleBot(token='6584407391:AAFGpfJ9Ip82G8g5pAM3T-X_4k2MrqlFRdg')


def get_id(message):
    return message.from_user.id


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    chat_id = get_id(message)

    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(text='Инфо'))
    markup.add(KeyboardButton(text='Техподдержка'))

    bot.send_message(chat_id=chat_id, text='Привет!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Инфо')
def info_message(message: Message):
    chat_id = get_id(message)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Инфо', callback_data='1'))
    markup.add(InlineKeyboardButton(text='Техподдержка', callback_data='2'))

    bot.send_message(chat_id=chat_id, text='Информация о боте!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == '1')
def info_subbotton(call: CallbackQuery):
    chat_id = call.from_user.id

    bot.send_message(chat_id, 'ПРИПРИВЕТ!!!')
    bot.edit_message_text()


bot.infinity_polling()

# 10000 раз в секунду - есть что-то от тебя?

# да, привет



