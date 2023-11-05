from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext

from telegram_bot.states import PromouterStates
from telegram_bot.handlers.promouter_panel.main_promouter_panel import accepted_promouter_panel
from telegram_bot.repository.api_methods import get_all_events
from telegram_bot.repository import api_methods



@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Посмотреть количество билетов в наличии")
async def identify_promouter(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(PromouterStates.choose_event_for_participants_registration)
    await message.answer(text='Выберите мероприятие, на которое вы хотите зарегистрировать участника',
                         reply_markup=markup)

