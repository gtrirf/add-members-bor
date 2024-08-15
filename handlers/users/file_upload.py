from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp
import os
from handlers.groups.addmembers import process_and_add_users
from aiogram.utils.exceptions import BotBlocked
import logging

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    waiting_for_file = State()
    waiting_for_group_selection = State()

@dp.message_handler(commands='addmembers')
async def start_add_members(message: types.Message):
    try:
        await message.answer("Iltimos, telefon raqamlarini o'z ichiga olgan Excel faylini yuklang")
        await Form.waiting_for_file.set()
    except BotBlocked:
        logging.warning(f"Cannot send message to {message.from_user.id}, bot was blocked by the user.")
    except Exception as e:
        logging.error(f"Error while handling /addmembers command: {e}")

@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=Form.waiting_for_file)
async def handle_file_upload(message: types.Message, state: FSMContext):
    try:
        file_name = message.document.file_name
        if not file_name.endswith(('.xlsx', '.xls')):
            await message.answer("Iltimos, faqat Excel fayllarini yuklang (.xlsx, .xls).")
            return

        file_path = f"data/{file_name}"
        await message.document.download(file_path)
        await state.update_data(file_path=file_path)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("@eh_1group"), KeyboardButton("@URGUTKUTUBXONA"))

        await message.answer("A'zolar qo'shiladigan guruhni tanlang:", reply_markup=markup)
        await Form.waiting_for_group_selection.set()

    except Exception as e:
        logging.error(f"Error while handling file upload: {e}")
        await message.answer(f"Failed to upload the file. Reason: {e}")

@dp.message_handler(state=Form.waiting_for_group_selection)
async def handle_group_selection(message: types.Message, state: FSMContext):
    selected_group = message.text
    user_data = await state.get_data()
    file_path = user_data.get('file_path')

    if not os.path.exists(file_path):
        await message.answer("Fayl topilmadi. Iltimos, qayta yuklang.")
        await state.finish()
        return

    try:
        await process_and_add_users(file_path, selected_group)
        await message.answer(f"Processing complete. Members added to {selected_group}.")
    except Exception as e:
        logging.error(f"Error during group member addition: {e}")
        await message.answer(f"Failed to add members. Reason: {e}")

    await state.finish()
