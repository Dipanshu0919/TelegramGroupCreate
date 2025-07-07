import asyncio
import os
import random
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest

# ========= CONFIGURATION =========
try:
    api_id_list = list(map(int, os.environ.get("API_IDS").split(",")))
    api_hash_list = os.environ.get("API_HASHS").split(",")
    string_session_list = os.environ.get("STRING_SESSIONS").split(",")
except Exception as env_error:
    print(f"[!] Failed to load environment variables: {env_error}")
    api_id_list, api_hash_list, string_session_list = [], [], []

second_user_username = 'missrose_bot'
image_path = "screenshot.png"
image_caption = 'Welcome to the group! 🎉'
random_messages = ["Hi", "Hello", "Yo", "What's up?", "How's it going?"]
today = datetime.now().strftime('%Y-%m-%d')

async def create_group(client):
    try:
        title = f"{today}"
        print(f"\n==> Creating supergroup: {title}")

        result = await client(CreateChannelRequest(
            title=title,
            about=f"Created on {today}",
            megagroup=True
        ))
        group = result.chats[0]
        print(f"[+] Created supergroup (ID: {group.id})")

        try:
            user = await client.get_entity(second_user_username)
            await client(InviteToChannelRequest(channel=group, users=[user]))
            print("    → Invited second user")
        except Exception as e:
            print(f"[!] Error inviting user: {e}")

        for _ in range(5):
            try:
                await client.send_file(group, image_path, caption=image_caption)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[!] Error sending image: {e}")
        print("    → Sent 5 images")

        for _ in range(5):
            try:
                await client.send_message(group, random.choice(random_messages))
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[!] Error sending message: {e}")
        print("    → Sent 5 text messages")

    except Exception as e:
        print(f"[!] Error in group creation: {e}")

async def main():
    if not api_id_list or not api_hash_list or not string_session_list:
        print("[!] Skipping run because environment variables are missing or empty.")
        return

    for x, y, z in zip(api_id_list, api_hash_list, string_session_list):
        try:
            async with TelegramClient(StringSession(z), x, y) as client:
                for _ in range(2):  # Create 2 groups per account
                    try:
                        await create_group(client)
                    except Exception as e:
                        print(f"[!] Error while creating group: {e}")
        except Exception as e:
            print(f"[!] Client session error: {e}")

try:
    asyncio.run(main())
except Exception as e:
    print(f"[!] Fatal error in asyncio loop: {e}")
