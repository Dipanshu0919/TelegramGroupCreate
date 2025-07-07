import asyncio
import os
import random
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest

# ========= CONFIGURATION =========
api_id_list = list(map(int, os.environ.get("API_ID").split(",")))
api_hash_list = os.environ.get("API_HASH").split(",")
string_session_list = os.environ.get("STRING_SESSION").split(",")

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

asyncio.run(main())
