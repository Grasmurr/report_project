from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telegram_bot.repository import api_methods

import datetime


async def get_id_from_message(message: Message):
    return message.from_user.id


def create_keyboard_buttons(*args):
    builder = ReplyKeyboardBuilder()
    for i in args:
        builder.button(text=i)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


async def generate_next_ticket_number(event_name, ticket_type):
    event_info = await api_methods.get_event_by_name(event_name)
    print(event_info)
    start_point = event_info['data'][0]['ticket_number_start']
    tickets = await api_methods.get_ticket_by_number_or_type(event=event_name, ticket_type=ticket_type)
    if not tickets['data']:
        if ticket_type == 'Обычный':
            return start_point
        elif ticket_type == 'Bundle':
            return start_point + 1000
        elif ticket_type == 'Прайм':
            return start_point + 10000
        else:
            return start_point + 12000
    elif tickets['data']:
        tickets_data = tickets['data']
        mx_num = max([i['ticket_number'] for i in tickets_data])
        if ticket_type == 'Обычный':
            if mx_num == start_point + 200:
                return start_point + 350
            elif mx_num == start_point + 700:
                return start_point + 800
            return mx_num + 1
        elif ticket_type == 'Bundle':
            if mx_num == start_point + 1200:
                return start_point + 1350
            elif mx_num == start_point + 1700:
                return start_point + 1800
            return mx_num + 1
        elif ticket_type == 'Прайм':
            if mx_num == start_point + 10200:
                return start_point + 10350
            elif mx_num == start_point + 10700:
                return start_point + 10800
            return mx_num + 1
        else:
            if mx_num == start_point + 12200:
                return start_point + 12350
            elif mx_num == start_point + 12700:
                return start_point + 12800
            return mx_num + 1


async def define_refund_percent(event_name):
    event_info = await api_methods.get_event_by_name(event_name)
    event_date = event_info['data'][0]['date_of_event']
    target_date = datetime.datetime.strptime(event_date, '%Y-%m-%d')
    today = datetime.datetime.today()
    difference = (target_date - today).days + 1
    coefficent = 1
    if difference >= 10:
        return coefficent
    elif difference >= 5:
        return 0.5
    elif difference >= 3:
        return 0.3
    return False
