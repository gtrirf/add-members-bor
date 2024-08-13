from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(Command('start'))
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
