from pyrogram import Client

# Replace these with your own values
API_ID = '23710152'
API_HASH = '67f5a7e280baf4d65c3a54e79225c5b0'
PHONE_NUMBER = '+447300384570'

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

async def add_user_to_group(group_username, user_id):
    async with app:
        try:

            await app.add_chat_members(group_username, user_id)
            print(f"User {user_id} added to {group_username}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    group_username = "@eh_1group"
    user_id = 1948824452
    app.run(add_user_to_group(group_username, user_id))
