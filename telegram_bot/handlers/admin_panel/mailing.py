from telegram_bot.loader import dp, bot
from aiogram.types import \
    (Message,
    ReplyKeyboardRemove
     )
from telegram_bot.helpers import chat_backends
from aiogram import F
from aiogram.fsm.context import FSMContext
from telegram_bot.states import AdminStates

from telegram_bot.repository import api_methods

from telegram_bot.handlers.admin_panel.main_admin_menu import admin_menu

ADMIN_ID = 305378717

@dp.message(AdminStates.main, F.text == 'Рассылка')
async def start_mailing(message: Message, state: FSMContext):
    buttons = chat_backends.create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
    await message.answer('Хорошо! Выберите в каком формате вы хотите отправить рассылку:', reply_markup=buttons)
    await state.set_state(AdminStates.begin_mailing)


@dp.message(AdminStates.begin_mailing, F.text == 'Назад')
async def back_to_admin_menu(message: Message, state: FSMContext):
    await admin_menu(message, state)


@dp.message(AdminStates.begin_mailing)
async def back_to_admin_menu(message: Message, state: FSMContext):
    type_to_mail = message.text
    if type_to_mail not in ['Текст', 'Фото', 'Файл']:
        buttons = chat_backends.create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
        await message.answer('Кажется, вы выбрали что-то не из кнопок. Пожалуйста, воспользуйтесь кнопкой ниже:',
                             reply_markup=buttons)
        return
    buttons = chat_backends.create_keyboard_buttons('Назад')
    if type_to_mail == 'Текст':
        await state.set_state(AdminStates.mailing_with_text)
        await message.answer('Хорошо! Отправьте текст, который вы собираетесь отправить промоутерам:',
                             reply_markup=buttons)
    elif type_to_mail == 'Фото':
        await state.set_state(AdminStates.mailing_with_photo)
        await message.answer('Хорошо! Отправьте фото, которое вы собираетесь отправить промоутерам (с подписью):',
                             reply_markup=buttons)
    else:
        await state.set_state(AdminStates.mailing_with_file)
        await message.answer('Хорошо! Отправьте файл, который вы собираетесь отправить промоутерам (с подписью):',
                             reply_markup=buttons)


@dp.message(AdminStates.mailing_with_photo, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)



@dp.message(AdminStates.mailing_with_text, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)



@dp.message(AdminStates.mailing_with_file, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await start_mailing(message, state)


@dp.message(AdminStates.mailing_with_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    await state.update_data(mailing_type='Фото', photo_id=photo_id, caption=caption)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такое фото с такой подписью?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id, caption=caption)


@dp.message(AdminStates.mailing_with_file, F.document)
async def handle_photo(message: Message, state: FSMContext):
    file_id = message.document.file_id
    caption = message.caption
    await state.update_data(mailing_type='Файл', file_id=file_id, caption=caption)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой файл с такой подписью?', reply_markup=buttons)
    await message.answer_document(document=file_id, caption=caption)


@dp.message(AdminStates.mailing_with_text, F.text == 'Подтвердить')
async def handle_text(message: Message, state: FSMContext):
    await mail_promouters(state)
    await admin_menu(message, state)


@dp.message(AdminStates.mailing_with_text)
async def handle_text(message: Message, state: FSMContext):
    ans = message.text
    await state.update_data(mailing_type='Текст', text_to_mail=ans)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой текст?', reply_markup=buttons)
    await message.answer(ans)


@dp.message(AdminStates.mailing_with_file, F.text == 'Подтвердить')
async def start_file_mailing(message: Message, state: FSMContext):
    await mail_promouters(state)
    await admin_menu(message, state)


@dp.message(AdminStates.mailing_with_photo, F.text == 'Подтвердить')
async def start_photo_mailing(message: Message, state: FSMContext):
    await mail_promouters(state)
    await admin_menu(message, state)


async def mail_promouters(state: FSMContext):
    ids = await api_methods.get_all_promouters()
    data = await state.get_data()
    mailing_type = data['mailing_type']
    if mailing_type == 'Текст':
        content = data['text_to_mail']
    elif mailing_type == 'Фото':
        content = [data['photo_id'], data['caption']]
    else:
        content = [data['file_id'], data['caption']]
    for i in ids['data']:
        user_id = i['user_id']
        try:
            if mailing_type == 'Текст':
                await bot.send_message(chat_id=user_id, text=content)
            elif mailing_type == 'Фото':
                photo_id, caption = content
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=caption)
            elif mailing_type == 'Файл':
                file_id, caption = content
                await bot.send_document(chat_id=user_id, document=file_id, caption=caption)
        except:
            await bot.send_message(chat_id=ADMIN_ID, text=f'Не получилось отправить пользователю {user_id} '
                                                          f'({i["full_name"]})')


