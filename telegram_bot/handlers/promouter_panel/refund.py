from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove,
    CallbackQuery
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.states import PromouterStates
from telegram_bot.handlers.promouter_panel.main_promouter_panel import accepted_promouter_panel
from telegram_bot.repository.api_methods import get_all_events
from telegram_bot.repository import api_methods

from telegram_bot.gdrive.api_methods import update_gdrive

from telegram_bot.assets.configs import config

import re


@dp.message(PromouterStates.main_accepted_promouter_panel, F.text == "Оформить возврат")
async def choose_event_for_refund(message: Message, state: FSMContext):
    events = await get_all_events()
    event_names = [event['name'] for event in events['data'] if event['is_hidden'] is False]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(PromouterStates.choose_event_for_participants_refund)
    await message.answer(text='Выберите мероприятие, на которое был куплен билет',
                         reply_markup=markup)


@dp.message(PromouterStates.choose_event_for_participants_refund, F.text == "Назад")
async def ticket_refund_choose_event_back(message: Message, state: FSMContext):
    await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.choose_event_for_participants_refund)
async def ticket_refund_choose_type(message: Message, state: FSMContext):
    event_to_refund = message.text
    exists = await api_methods.get_event(event_to_refund)
    if exists:
        await state.update_data(event_to_refund=event_to_refund)
        await state.set_state(PromouterStates.choose_ticket_type_for_refund)
        markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Депозит', 'Назад')
        await message.answer(text='Выберите тип билета, который вы хотите вернуть:', reply_markup=markup)
    else:
        events = await api_methods.get_all_events()
        event_names = [event['name'] for event in events['data']]
        markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
        await message.answer(text='Кажется, вы случайно нажали не на ту кнопку. Выберите мероприятие из списка кнопок:',
                             reply_markup=markup)


@dp.message(PromouterStates.choose_ticket_type_for_refund, F.text == "Назад")
async def ticket_type_choose_event_back(message: Message, state: FSMContext):
    await choose_event_for_refund(message, state)


@dp.message(PromouterStates.choose_ticket_type_for_refund)
async def ticket_refund_choose_event(message: Message, state: FSMContext):
    type_to_refund = message.text
    if type_to_refund in ['Обычный', 'Прайм', 'Депозит']:
        await state.update_data(type_to_refund=type_to_refund)
        await state.set_state(PromouterStates.enter_number_of_ticket_for_refund)
        await message.answer(text='Пожалуйста, введите номер билета, который вы хотите вернуть:',
                             reply_markup=ReplyKeyboardRemove())
    else:
        markup = chat_backends.create_keyboard_buttons('Обычный', 'Прайм', 'Депозит', 'Назад')
        await message.answer(text='Кажется, вы случайно нажали не на ту кнопку. Выберите тип билета из списка кнопок:',
                             reply_markup=markup)


@dp.message(PromouterStates.enter_number_of_ticket_for_refund, F.text == 'Назад')
async def back_to_ticket_type(message: Message, state: FSMContext):
    await ticket_type_choose_event_back(message, state)


@dp.message(PromouterStates.enter_number_of_ticket_for_refund)
async def handle_ticket_number(message: Message, state: FSMContext):
    number_to_refund = message.text
    try:
        number_to_refund = int(number_to_refund)
    except:
        await message.answer('Кажется, вы ввели не номер билета! Пожалуйста, введите номер цифрами. Например: 150')
    data = await state.get_data()

    exists = await api_methods.get_ticket_by_number_or_type(event=data['event_to_refund'],
                                                            ticket_number=number_to_refund,
                                                            ticket_type=data['type_to_refund'])
    print(exists)
    if not exists['data']:
        await message.answer('Кажется, такого билета нет в базе!\n\nПопробуйте ввести данные заново!')
        await choose_event_for_refund(message, state)
    elif exists['data'][0]['is_refunded']:
        await message.answer("Этот билет уже был возвращен")
        await accepted_promouter_panel(message, state)
    elif exists['data']:
        id_data = exists
        await state.update_data(number_to_refund=number_to_refund)
        markup = chat_backends.create_keyboard_buttons('Продолжить', 'Назад')

        name = id_data['data'][0]['ticket_holder_name']
        surname = id_data['data'][0]['ticket_holder_surname']

        coefficent_to_return = await chat_backends.define_refund_percent(data['event_to_refund'])
        if coefficent_to_return:
            return_sum = int(id_data["data"][0]["price"] * coefficent_to_return)
            await state.update_data(return_sum=return_sum)
            await message.answer(f'Вы собираетесь подать заявку на возврат билета №{number_to_refund}.\n'
                                 f'\nИмя: {name}\nФамилия: {surname}\n'
                                 f'Тип билета: {data["type_to_refund"]}\n\nСумма для возврата: {return_sum}'
                                 f'\n\nПродолжить?', reply_markup=markup)
            await state.set_state(PromouterStates.confirm_ticket_data_for_refund)
        else:
            await message.answer('До мероприятия осталось менее 3 дней, поэтому возврат невозможен!')
            await accepted_promouter_panel(message, state)


@dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == 'Назад')
async def final_the_refund_back(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.enter_number_of_ticket_for_refund)
    await message.answer(text='Пожалуйста, введите номер билета, который вы хотите вернуть:',
                         reply_markup=ReplyKeyboardRemove())


@dp.message(PromouterStates.confirm_ticket_data_for_refund)
async def final_the_refund(message: Message, state: FSMContext):
    if message.text == 'Продолжить':

        data = await state.get_data()
        return_sum = data['return_sum']
        event_name = data['event_to_refund']
        number_to_refund = data['number_to_refund']
        type_to_refund = data['type_to_refund']

        id_data = await api_methods.get_ticket_by_number_or_type(event=event_name,
                                                                 ticket_number=number_to_refund,
                                                                 ticket_type=type_to_refund)

        name = id_data['data'][0]['ticket_holder_name']
        surname = id_data['data'][0]['ticket_holder_surname']

        promouter_data = await api_methods.get_promouter(message.from_user.id)
        promouter_name = promouter_data['data'][0]['full_name']

        builder = InlineKeyboardBuilder()
        builder.button(text='Подтвердить', callback_data=f'confirm_{message.from_user.id}')
        builder.button(text='Отказать', callback_data=f'refuse_{message.from_user.id}')
        markup = builder.as_markup()

        await bot.send_message(chat_id=config.ADMIN_ID,
                               text=f'От представителя {promouter_name} пришла заявка на возврат '
                                    f'билета на мероприятие: {event_name}\nТип билета: {type_to_refund}\nНомер '
                                    f'билета: {number_to_refund}\nИмя: {name}\nФамилия: {surname}\n\nСумма для '
                                    f'возврата: {return_sum}\n\nПодтвердить?', reply_markup=markup)

        await message.answer('Заявка была отправлена админу! В скором времени вы получите ответ!')
        await accepted_promouter_panel(message, state)

    else:
        markup = chat_backends.create_keyboard_buttons('Продолжить', 'Назад')
        await message.answer('Пожалуйста, воспользуйтесь кнопками ниже:', reply_markup=markup)


@dp.callback_query(lambda call: call.data.startswith('confirm') or call.data.startswith('refuse'))
async def handle_refund(call: CallbackQuery, state: FSMContext):
    ans, promouter_id = call.data.split('_')
    data = call.message.text

    try:

        ticket_number = int(re.search(r'Номер билета: (\d+)', data).group(1))
        refund_amount = int(re.search(r'Сумма для возврата: (\d+)', data).group(1))
        ticket_type = re.search(r'Тип билета: (.+)', data).group(1)
        event_name = re.search(r'мероприятие: (.+)', data).group(1)

        name = re.search(r'Имя: (.+)', data).group(1)
        surname = re.search(r'Фамилия: (.+)', data).group(1)

        print(ticket_number, refund_amount, ticket_type, event_name)

        print(data)
        if ans == 'refuse':
            await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
            await bot.send_message(chat_id=call.message.chat.id, text='Вы отклонили эту заявку!')
            await bot.send_message(chat_id=promouter_id, text=f'Ваша заявка на возврат билета для участника {name} '
                                                              f'{surname} с номером билета {ticket_number} '
                                                              f'была отклонена!')
        else:
            await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
            await bot.send_message(chat_id=call.message.chat.id, text='Вы подтвердили эту заявку!')

            builder = InlineKeyboardBuilder()
            builder.button(text='Вернул!', callback_data=f'rfnded_{promouter_id}')
            markup = builder.as_markup()

            await bot.send_message(chat_id=promouter_id, text=f'Ваша заявка на возврат билета для участника {name} '
                                                              f'{surname} с номером билета {ticket_number} '
                                                              f'была одобрена! \n\nВам нужно вернуть клиенту сумму '
                                                              f'{refund_amount}р.', reply_markup=markup)

            id_data = await api_methods.get_ticket_by_number_or_type(event=event_name,
                                                                     ticket_number=ticket_number,
                                                                     ticket_type=ticket_type)

            new_sum = id_data["data"][0]["price"] - refund_amount

            await api_methods.return_ticket(ticket_number=ticket_number,
                                            event=event_name,
                                            ticket_type=ticket_type, new_price=new_sum)

            field = 'nm_usual' if ticket_type == 'Обычный' else 'nm_prime' if ticket_type == 'Прайм' else 'nm_deposit'
            await api_methods.update_ticket_number(event_name=event_name, action='increment', field=field)

            ticket_info = await api_methods.get_ticket_by_number_or_type(event=event_name)

            await update_gdrive(event_name, ticket_info)
    except:
        await bot.send_message(chat_id=call.message.chat.id, text='Что-то пошло не так, обратитесь к разработчикам!')


@dp.callback_query(lambda call: call.data.startswith('rfnded'))
async def handle_refund_from_promouter(call: CallbackQuery, state: FSMContext):
    ans, promouter_id = call.data.split('_')
    data = call.message.text

    participant_name_match = re.search(r"участника\s+([А-Я][а-я]+\s+[А-Я][а-я]+)", data).group(1)
    ticket_number_match = int(re.search(r"номером билета\s+(\d+)", data).group(1))
    refund_amount_match = int(re.search(r"сумму\s+(\d+)р", data).group(1))

    promouter = await api_methods.get_promouter(promouter_id)
    name = promouter['data'][0]['full_name']
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot.send_message(chat_id=config.ADMIN_ID, text=f'Представитель {name} вернул участнику '
                                                         f'{participant_name_match} с номером билета '
                                                         f'{ticket_number_match} '
                                                         f'сумму {refund_amount_match}р.!')
    await bot.send_message(chat_id=promouter_id, text='Спасибо! Сообщение было отправлено админу!')


#             markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
#                                                        "Оформить возврат",
#                                                        "Посмотреть количество билетов в наличии")
#             await message.answer(text=f"Ваша заявка на возврат билета одобрена администратором. "
#                                       f"Пожалуйста, верните {price} рублей покупателю данного билета.",
#                                  reply_markup=markup)
#             await state.set_state(PromouterStates.main_accepted_promouter_panel)
#         # else:
#         #     markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
#         #                                                    "Оформить возврат")
#         #     await message.answer(text=f"Ваша заявка на возврат билета не одобрена администратором. "
#         #                               f"Пожалуйста, обратитесь к администратору (@URL) для уточнения причины.",
#         #                          reply_markup=markup)

#
# data = await state.get_data()
# await api_methods.return_ticket(ticket_number=data['number_to_refund'],
#                                 event=data['event_to_refund'],
#                                 ticket_type=data['type_to_refund'], new_price=data['return_sum'])
# field = 'nm_usual' if data['type_to_refund'] == 'Обычный' else 'nm_prime' if data['type_to_refund'] == 'Прайм' else 'nm_deposit'
# await api_methods.update_ticket_number(event_name=data['event_to_refund'], action='increment', field=field)
# await message.answer('Возврат произошел успешно!')
#
# ticket_info = await api_methods.get_ticket_by_number_or_type(data['event_to_refund'])
#
# await update_gdrive(data['event_to_refund'], ticket_info)
#
# await accepted_promouter_panel(message, state)




#
# @dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Назад")
# async def back_from_confirm_ticket_data_for_refund(message: Message, state: FSMContext):
#     await enter_number_of_ticket_for_refund(message, state)
#
#
# @dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Подтвердить заявку на возврат")
# async def refund_ends(message: Message, state: FSMContext):
#     data = await state.get_data()
#     ticket_number_for_refund = data['ticket_number_for_refund']
#
#     if False:
#         pass
# # TODO: автоматический чек на существование в целом такого билета в базе
#
#     else:
#         await message.answer(text=f"Ваша заявка на возврат билета отправлена администратору. "
#                               f"Пожалуйста, дождитесь одобрения возврата от него.")
#
# # TODO: отправить сообщение админу
#         await state.set_state(PromouterStates.get_admin_confirmation_to_refund)
#
# @dp.message(PromouterStates.get_admin_confirmation_to_refund)
# async def refund_confirmation(message: Message, state: FSMContext):
#         # if:
#
#
#         # ticket = await get_ticket_by_number(ticket_number_for_refund)
#     # if not ticket:
#     #     await message.answer(text='Извините, билет с таким номером не найден. Попробуйте еще раз.', reply_markup = 'Назад')
#     #     return
#
#
# # @dp.message(PromouterStates.confirm_ticket_data_for_refund, F.text == "Подтвердить возврат")
# # async def refund_ends(message: Message, state: FSMContext):
# #     markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
# #                                                    "Оформить возврат")
# #     await message.answer(text='Спасибо! Возврат билета оформлен', reply_markup=markup)
# #     await state.set_state(PromouterStates.main_accepted_promouter_panel)

