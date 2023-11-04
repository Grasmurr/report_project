from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
     ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository.api_methods import create_event, get_all_events
from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

from telegram_bot.repository import api_methods

@dp.message(AdminStates.manage_events, F.text == 'Изменить ценовой диапазон')
async def change_price_range(message: Message, state: FSMContext):
    events = await api_methods.get_all_events()
    event_names = [event['name'] for event in events['data']]
    markup = chat_backends.create_keyboard_buttons(*event_names, 'Назад')
    await state.set_state(AdminStates.choose_event_to_change_price_range)
    await message.answer("Выберите мероприятие для изменения ценового диапазона:", reply_markup=markup)


@dp.message(AdminStates.choose_event_to_change_price_range)
async def enter_event_name_for_price(message: Message, state: FSMContext):
    event_name = message.text
    if event_name == 'Назад':
        await admin_menu(message, state)
        return

    events = await api_methods.get_all_events()
    if event_name not in [event['name'] for event in events['data']]:
        await message.answer("Событие не найдено. Попробуйте снова.")
        return

    await state.update_data(event_name=event_name)
    await state.set_state(AdminStates.enter_price_range_for_change)
    await message.answer('Хорошо! введите список цен, которое вы хотите предусмотреть:'
                         '\n\nНапример:\n1500\n2000\n2500\n\nКаждое с новой строки!', reply_markup=ReplyKeyboardRemove())


@dp.message(AdminStates.enter_price_range_for_change)
async def handle_price_range_for_change(message: Message, state: FSMContext):
    rng = message.text.split('\n')
    print(rng)
    if not rng:
        await message.answer('Попробуйте ввести список еще раз')
    try:
        rng = [int(i) for i in rng]
        print(rng)
        await state.update_data(prices_range=rng)
        data = await state.get_data()
        str_prices = [str(i) for i in rng]
        buttons = chat_backends.create_keyboard_buttons('Продолжить', 'Ввести данные заново')
        await message.answer(f'Хорошо! Для мероприятия {data["event_name"]}\n'
                             f'Ценовой диапазон теперь выглядит вот так: {"-".join(str_prices)}',
                             reply_markup=buttons)
        await state.set_state(AdminStates.saving_or_editing_from_the_beginning_price_range)
    except:
        await message.answer('Попробуйте ввести список еще раз')


@dp.message(AdminStates.saving_or_editing_from_the_beginning_price_range)
async def final_price_range(message: Message, state: FSMContext):
    if message.text == 'Продолжить':
        event_data = await state.get_data()
        data = await state.get_data()
        str_prices = [str(i) for i in data["prices_range"]]
        await api_methods.update_event_data(name=event_data['event_name'], prices=data["prices_range"])
        await message.answer(f'Хорошо! Ценовой диапазон теперь выглядит вот так: {"-".join(str_prices)}')
        await admin_menu(message, state)
    elif message.text == 'Начать заново':
        await message.answer("Отмена операции.")
        await change_price_range(message, state)
    else:
        await message.answer('Кажется, вы ввели что-то не то. Попробуйте использовать кнопки:')


