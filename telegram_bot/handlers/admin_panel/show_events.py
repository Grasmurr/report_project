from telegram_bot.loader import dp, bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import \
    (Message,
     CallbackQuery,
     KeyboardButton,
     ReplyKeyboardMarkup,
     InlineKeyboardMarkup,
     InlineKeyboardButton,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.enums.content_type import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from telegram_bot.states import AdminStates


from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

from telegram_bot.gdrive.api_methods import update_gdrive

from telegram_bot.repository import api_methods


@dp.message(AdminStates.main, F.text == 'Скрыть/показать мероприятие')
async def event_delete_start(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.choose_event_to_show)
    await message.answer(text='Выберите мероприятие, которое вы хотите показать/скрыть для промоутеров:',
                         reply_markup=markup)


@dp.message(AdminStates.choose_event_to_show, F.text == "Назад")
async def event_delete_start_back(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.choose_event_to_show)
async def choose_action_for_event_for_promouters(message: Message, state: FSMContext):
    event_name = message.text
    await state.update_data(event_name=event_name)
    markup = chat_backends.create_keyboard_buttons('Скрыть', 'Показать', 'Назад')
    await message.answer('Хорошо! Вы хотите скрыть или показать это мероприятие для промоутеров?', reply_markup=markup)
    await state.set_state(AdminStates.choose_action_to_show_or_hide)


@dp.message(AdminStates.choose_action_to_show_or_hide, F.text == "Назад")
async def choose_action_for_event_for_promouters_back(message: Message, state: FSMContext):
    await event_delete_start(message, state)


@dp.message(AdminStates.choose_action_to_show_or_hide)
async def handle_action_for_event_to_hide_or_show(message: Message, state: FSMContext):
    action = message.text
    if action == 'Скрыть':
        data = await state.get_data()
        await api_methods.update_event_visibility(data['event_name'], is_hidden=True)
        await message.answer(f'Хорошо! Вы скрыли мероприятие {data["event_name"]} для промоутеров!')
    elif action == 'Показать':
        data = await state.get_data()
        await api_methods.update_event_visibility(data['event_name'], is_hidden=False)
        await message.answer(f'Хорошо! Вы показали мероприятие {data["event_name"]} для промоутеров!')
    else:
        markup = chat_backends.create_keyboard_buttons('Скрыть', 'Показать', 'Назад')
        await message.answer('Кажется, вы нажали не туда! Попробуйте воспользоваться одной из кнопок:',
                             reply_markup=markup)
