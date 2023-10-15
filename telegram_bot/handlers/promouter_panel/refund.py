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


@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Оформить возврат")
async def choose_event_for_refund(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons('Мероприятие 1', 'Мероприятие 2', 'Назад')
    await state.set_state(PromouterStates.choose_event_for_participants_refund)
    await message.answer(text='Выберите мероприятие, на которое был куплен билет',
                         reply_markup=markup)


@dp.message(PromouterStates.choose_event_for_participants_refund, F.text == "Назад")
async def back_from_refund(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.choose_event_for_participants_refund)
async def choose_ticket_type_for_refund(message: Message, state: FSMContext):
    event_for_refund = message.text
    data = await state.get_data()
    await state.update_data(event_for_refund=event_for_refund)
    markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Назад')
    await state.set_state(PromouterStates.choose_ticket_type_for_refund)
    await message.answer(text='Выберите тип билета',
                         reply_markup=markup)


@dp.message(PromouterStates.choose_ticket_type_for_refund, F.text == "Назад")
async def back_from_choose_ticket_type_for_refund(message: Message, state: FSMContext):
    await choose_event_for_refund(message, state)


@dp.message(PromouterStates.choose_ticket_type_for_refund)
async def enter_number_of_ticket_for_refund(message: Message, state: FSMContext):
    ticket_type_for_refund = message.text
    data = await state.get_data()
    await state.update_data(ticket_type_for_refund=ticket_type_for_refund)
    await state.set_state(PromouterStates.enter_number_of_ticket_for_refund)
    await message.answer(text='Введите номер билета', reply_markup=ReplyKeyboardRemove())


@dp.message(PromouterStates.enter_number_of_ticket_for_refund)
async def confirm_ticket_data_for_refund(message: Message, state: FSMContext):
    ticket_number_for_refund = message.text
    data = await state.get_data()
    await state.update_data(ticket_number_for_refund=ticket_number_for_refund)
    ticket_type_for_refund = data['ticket_type_for_refund']
    event_for_refund = data['event_for_refund']
    markup = chat_backends.create_keyboard_buttons('Подтвердить возврат', 'Назад')
    await state.set_state(PromouterStates.confirm_ticket_data_for_refund)
    await message.answer(
        text=f'Вы собираетесь оформить возврат билета №{ticket_number_for_refund} типа "{ticket_type_for_refund}" '
             f'на мероприятие "{event_for_refund}". '
             f'Подтвердить?',
        reply_markup=markup)


@dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Назад")
async def back_from_confirm_ticket_data_for_refund(message: Message, state: FSMContext):
    await enter_number_of_ticket_for_refund(message, state)


@dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Подтвердить возврат")
async def refund_ends(message: Message, state: FSMContext):
    markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат")
    await message.answer(text='Спасибо! Возврат билета оформлен', reply_markup=markup)
    await state.set_state(PromouterStates.accepted_promouter_panel)

