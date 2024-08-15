from pyrogram import Client
from utils.db_api.database import get_db
from utils.db_api.models import UserData
from environs import Env
import logging
from pyrogram.raw.types import InputPhoneContact


env = Env()
env.read_env()

API_ID = env.str('API_ID')
API_HASH = env.str('API_HASH')
PHONE_NUMBER = '+447300384570'


app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

async def add_user_to_group(group_username, user_id):
    try:
        await app.add_chat_members(group_username, user_id)
        print(f"User {user_id} added to {group_username}")
    except Exception as e:
        logging.error(f"Error adding user to group: {e}")



async def get_user_id_from_phone(phone_number):
    try:
        contacts = [InputPhoneContact(client_id=0, phone=phone_number, first_name="User", last_name="")]
        result = await app.import_contacts(contacts)
        if result.users:
            return result.users[0].id
        else:
            logging.info(f"No user found with phone number: {phone_number}")
            return None
    except Exception as e:
        logging.error(f"Error importing contacts: {e}")
        return None


def save_user_to_db(db, telegram_user_id, phone_number):
    new_user = UserData(telegram_user_id=telegram_user_id, phone_number=phone_number)
    db.add(new_user)
    db.commit()


async def process_and_add_users(file_path, group_username):
    from handlers.users.excel_read import process_file

    db = next(get_db())
    phone_numbers = process_file(file_path)

    await app.start()

    try:
        for phone_number in phone_numbers:
            user_in_db = db.query(UserData).filter(UserData.phone_number == phone_number).first()

            if user_in_db:
                print(f"User with phone number {phone_number} already in the database.")
            else:
                user_id = await get_user_id_from_phone(phone_number)
                if user_id:
                    try:
                        print(f"Attempting to add user {user_id} to group {group_username}")
                        await add_user_to_group(group_username, user_id)
                        save_user_to_db(db, user_id, phone_number)
                        print(f"User {phone_number} added to group and saved to database.")
                    except Exception as e:
                        if "CHAT_ADMIN_REQUIRED" in str(e):
                            special_account_username = "@iron_furyy"
                            invite_link = f"https://t.me/{special_account_username}"
                            print(f"Group access is not open. Please add the special account manually: {invite_link}")
                        else:
                            logging.error(f"Error adding user to group: {e}")
                            print(f"Failed to add user {phone_number} to group {group_username}. Error: {e}")
                else:
                    print(f"User ID for phone number {phone_number} could not be retrieved.")
    finally:
        await app.stop()
