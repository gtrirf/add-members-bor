import logging
from aiogram import Dispatcher
from data.config import ADMINS
from aiogram.utils.exceptions import BotBlocked


# async def on_startup_notify(dp: Dispatcher):
#     for admin in ADMINS:
#         try:
#             await dp.bot.send_message(admin, "Bot ishga tushdi")
#
#         except Exception as err:
#             logging.exception(err)


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
        except BotBlocked:
            print("The bot was blocked by the user, can't send the message.")
        except Exception as e:
            print(f"Failed to send startup notification: {e}")
