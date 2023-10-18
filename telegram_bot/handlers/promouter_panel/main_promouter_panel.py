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




@dp.message(PromouterStates.begin_registration)
async def identify_promouter(message: Message, state: FSMContext):
    # if message in data:
    await message.answer(f'Хорошо! Для идентификации, пожалуйста,'
                         f' введите свои имя и фамилию в формате:\n \n"Имя Фамилия"',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(PromouterStates.enter_initials)


@dp.message(PromouterStates.enter_initials)
async def identify_promouter_number(message: Message, state: FSMContext):
    print(message.text)
    if len(message.text.split()) == 2:
        await state.set_state(PromouterStates.waitng_for_admin_accept)
        await message.answer(f'Спасибо! Введите, пожалуйста, свой номер телефона в формате "89991234567"',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Пожалуйста, введите имя и фамилию в формате "Иван Иванов"')


@dp.message(PromouterStates.waitng_for_admin_accept)
async def waiting_for_admin_accept(message: Message, state: FSMContext):

    if message.text.isdigit() and len(message.text.split()) == 1:
        await state.set_state(PromouterStates.accepted_promouter_panel)

        builder = InlineKeyboardBuilder()
        builder.button(text='Подтвердить', callback_data=f'allow{message.from_user.id}')
        builder.button(text='Отказать', callback_data=f'decline{message.from_user.id}')
        markup = builder.as_markup()

        await bot.send_message(chat_id=305378717,
                                 text='Подтвердить регистрацию промоутера?',
                                 reply_markup=markup)

        await message.answer(f'Спасибо! Скоро админ проверит вашу заявку', reply_markup=ReplyKeyboardRemove())

    else:
        await message.answer(f'Пожалуйста, введите свой номер телефона в формате "89991234567"')


@dp.callback_query(PromouterStates.accepted_promouter_panel)
async def handle_admin_decision(call: CallbackQuery, state: FSMContext):
    ans = call.data
    if ans[:5] == 'allow':
        await bot.send_message(chat_id=ans[5:], text='Админ подтвердил вашу заявку!')
        await state.set_state(PromouterStates.main_accepted_promouter_panel)
        markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                       "Оформить возврат")
        await bot.send_message(chat_id=ans[5:],
                               text=f'Добро пожаловать в панель промоутера',
                               reply_markup=markup)
    else:
        await state.set_state(PromouterStates.begin_registration)
        markup = create_keyboard_buttons('Зарегистрироваться')
        await bot.send_message(chat_id=ans[7:],
                               text=f'Добро пожаловать в телеграм бот агентства Гамма! '
                             f'Для начала работы необходимо зарегистрироваться в качестве промоутера!',
                               reply_markup=markup)


async def accepted_promouter_panel(message: Message, state: FSMContext):
    await state.set_state(PromouterStates.main_accepted_promouter_panel)
    markup = chat_backends.create_keyboard_buttons("Зарегистрировать участника",
                                                   "Оформить возврат")
    await message.answer(text=f'Добро пожаловать в панель промоутера',
                           reply_markup=markup)

