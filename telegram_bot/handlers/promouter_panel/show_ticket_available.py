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
async def choose_event_for_information(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(PromouterStates.choose_event_for_info)
    await message.answer(text='Выберите мероприятие, о котором вы хотите получить информацию',
                         reply_markup=markup)

@dp.message(PromouterStates.choose_event_for_info, F.text == 'Назад')
async def back_from_choose_event_for_information(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)

@dp.message(PromouterStates.choose_event_for_info)
async def sending_information_about_event(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    if message.text not in event_names:
        await message.answer (text="Кажется вы нажали не туда. Пожалуйста, воспользуйтесь кнопками ниже для выбора мероприятия")
        return
    event = message.text
    event_data = await api_methods.get_event_by_name(event)
    nm_prime = event_data['data'][0]['nm_prime']
    nm_usual = event_data['data'][0]['nm_usual']
    nm_deposit = event_data['data'][0]['nm_deposit']

    markup = chat_backends.create_keyboard_buttons("Посмотреть данные о другом мероприятии", "Вернуться в меню")
    await message.answer (text=f"Данные о билетах в наличии для мероприятия «{event}»:\n\n"
                               f"Прайм: осталось {nm_prime}\n"
                               f"Обычные: осталось {nm_usual}\n"
                               f"Депозитные: осталось {nm_deposit}", reply_markup=markup)
    await state.set_state(PromouterStates.tickets_info_final)

@dp.message(PromouterStates.tickets_info_final, F.text == "Посмотреть данные о другом мероприятии")
async def see_another_event_info(message: Message, state: FSMContext):
    # await state.set_state(PromouterStates.main_accepted_promouter_panel)
    await choose_event_for_information(message, state)

@dp.message(PromouterStates.tickets_info_final, F.text == "Вернуться в меню")
async def back_from_sending_info_to_menu(message: Message, state: FSMContext):
        await state.set_state(PromouterStates.main_accepted_promouter_panel)
        markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                       "Оформить возврат",
                                                       "Посмотреть количество билетов в наличии")
        await message.answer(text=f'Добро пожаловать в панель промоутера',
                             reply_markup=markup)
