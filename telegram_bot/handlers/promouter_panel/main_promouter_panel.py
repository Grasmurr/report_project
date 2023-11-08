
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
from telegram_bot.states import PromouterStates
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.helpers.chat_backends import create_keyboard_buttons

from telegram_bot.repository import api_methods

from telegram_bot.assets.configs import config


@dp.message(PromouterStates.begin_registration)
async def identify_promouter(message: Message, state: FSMContext):
    # if message in data:
    await message.answer(f'Хорошо! Для идентификации, пожалуйста,'
                         f' введите свои имя и фамилию в формате:\n \n"Имя Фамилия"',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(PromouterStates.enter_initials)


@dp.message(PromouterStates.enter_initials)
async def identify_promouter_number(message: Message, state: FSMContext):
    button_phone = [KeyboardButton(text="Отправить номер", request_contact=True)]
    keyboard = ReplyKeyboardMarkup(keyboard=[button_phone], row_width=1, resize_keyboard=True)

    if len(message.text.split()) == 2:
        name = message.text
        user_id = message.from_user.id
        await api_methods.update_promouter(user_id=user_id, full_name=name)

        await state.set_state(PromouterStates.waitng_for_admin_accept)
        await message.answer(f'Спасибо! Для продолжения, отправьте нам номер телефона через кнопку ниже',
                             reply_markup=keyboard)
    else:
        await message.answer('Пожалуйста, введите имя и фамилию в формате "Иван Иванов"')


@dp.message(PromouterStates.waitng_for_admin_accept)
async def waiting_for_admin_accept(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number

        await state.set_state(PromouterStates.accepted_promouter_panel)

        usname = message.from_user.username
        if usname:
            usname = f'@{usname}'
        else:
            usname = 'Отсутствует'
        user_id = message.from_user.id

        await api_methods.update_promouter(user_id=user_id, username=usname, phone_number=int(phone_number))

        builder = InlineKeyboardBuilder()
        builder.button(text='Подтвердить', callback_data=f'allow{message.from_user.id}')
        builder.button(text='Отказать', callback_data=f'decline{message.from_user.id}')
        markup = builder.as_markup()

        await bot.send_message(chat_id=config.ADMIN_ID,
                               text=f'Подтвердить регистрацию представителя? \n\nИмя: {message.from_user.full_name}'
                                    f'\nUsername: {usname}'
                                    f'\nНомер телефона: +{int(phone_number)}',
                               reply_markup=markup)

        await message.answer(f'Спасибо! Скоро админ проверит вашу заявку', reply_markup=ReplyKeyboardRemove())

    else:
        button_phone = [KeyboardButton(text="Отправить номер", request_contact=True)]
        keyboard = ReplyKeyboardMarkup(keyboard=[button_phone], row_width=1, resize_keyboard=True)
        await message.answer(f'Пожалуйста, нажмите кнопку ниже для отправки номера телефона', reply_markup=keyboard)


@dp.callback_query(lambda call: call.data.startswith('allow') or call.data.startswith('decline'))
async def handle_admin_decision(call: CallbackQuery, state: FSMContext):
    ans = call.data
    user_id = ans[5:]

    if ans[:5] == 'allow':
        promouter = await api_methods.get_promouter(user_id)
        name = promouter['data'][0]['full_name']

        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=f'Вы подтвердили заявку представителя {name}!')

        await bot.send_message(chat_id=user_id, text='Админ подтвердил вашу заявку!')
        await state.set_state(PromouterStates.main_accepted_promouter_panel)
        markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                       "Оформить возврат",
                                                       "Посмотреть количество билетов в наличии")

        await bot.send_message(chat_id=user_id,
                               text=f'Добро пожаловать в панель представителя',
                               reply_markup=markup)
    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text='Вы отказали в заявке представителю!')
        await bot.send_message(chat_id=ans[7:], text='Админ отказал вам в заявке!')
        await api_methods.delete_promouter(ans[7:])
        await state.set_state(PromouterStates.begin_registration)
        markup = create_keyboard_buttons('Зарегистрироваться')
        await bot.send_message(chat_id=ans[7:],
                               text=f'Добро пожаловать в телеграм бот агентства Гамма! '
                               f'Для начала работы необходимо зарегистрироваться в качестве представителя!',
                               reply_markup=markup)


async def accepted_promouter_panel(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.main_accepted_promouter_panel)
    markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат",
                                                   "Посмотреть количество билетов в наличии")
    await message.answer(text=f'Добро пожаловать в панель представителя',
                         reply_markup=markup)

