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
from telegram_bot.repository.api_methods import delete_ticket


@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Оформить возврат")
async def choose_event_for_refund(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
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
        text=f'Вы собираетесь подать заявку на возврат билета №{ticket_number_for_refund} типа "{ticket_type_for_refund}" '
             f'на мероприятие "{event_for_refund}". '
             f'Подтвердить?',
        reply_markup=markup)


@dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Назад")
async def back_from_confirm_ticket_data_for_refund(message: Message, state: FSMContext):
    await enter_number_of_ticket_for_refund(message, state)


@dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Подтвердить заявку на возврат")
async def refund_ends(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_number_for_refund = data['ticket_number_for_refund']

    if False:
        pass
# TODO: автоматический чек на существование в целом такого билета в базе

    else:
        await message.answer(text=f"Ваша заявка на возврат билета отправлена администратору. "
                              f"Пожалуйста, дождитесь одобрения возврата от него.")

# TODO: отправить сообщение админу
        await state.set_state(PromouterStates.get_admin_confirmation_to_refund)

@dp.message(PromouterStates.get_admin_confirmation_to_refund)
async def refund_confirmation(message: Message, state: FSMContext):
        # if:
            price = 2000
            markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат")
            await message.answer(text=f"Ваша заявка на возврат билета одобрена администратором. "
                                      f"Пожалуйста, верните {price} рублей покупателю данного билета.",
                                 reply_markup=markup)
            await state.set_state(PromouterStates.main_accepted_promouter_panel)
        # else:
        #     markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
        #                                                    "Оформить возврат")
        #     await message.answer(text=f"Ваша заявка на возврат билета не одобрена администратором. "
        #                               f"Пожалуйста, обратитесь к администратору (@URL) для уточнения причины.",
        #                          reply_markup=markup)

        # ticket = await get_ticket_by_number(ticket_number_for_refund)
    # if not ticket:
    #     await message.answer(text='Извините, билет с таким номером не найден. Попробуйте еще раз.', reply_markup = 'Назад')
    #     return


# @dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Подтвердить возврат")
# async def refund_ends(message: Message, state: FSMContext):
#     markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
#                                                    "Оформить возврат")
#     await message.answer(text='Спасибо! Возврат билета оформлен', reply_markup=markup)
#     await state.set_state(PromouterStates.main_accepted_promouter_panel)

