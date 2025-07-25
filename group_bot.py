import asyncio, os
import random
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputPeerUser

# ========= CONFIGURATION =========
api_id = int(os.environ.get("API_ID"))  # ← Replace with your API ID
api_hash = os.environ.get("API_HASH")  # ← Replace with your API hash
string_session = os.environ.get("STRING_SESSION")
second_user_username = 'missrose_bot'
image_path = "screenshot.png"
image_caption = 'Welcome to the group! 🎉'
random_messages = ["Hi", "Hello", "Yo", "What's up?", "How's it going?"]

client = TelegramClient(StringSession(string_session), api_id, api_hash)
today = datetime.now().strftime('%Y-%m-%d')

async def create_group():
    try:
        title = f"{today}"
        print(f"\n==> Creating supergroup: {title}")

        # Create supergroup
        result = await client(CreateChannelRequest(
            title=title,
            about=f"Created on {today}",
            megagroup=True
        ))
        group = result.chats[0]
        print(f"[+] Created supergroup (ID: {group.id})")

        # Invite second user
        user = await client.get_entity(second_user_username)
        await client(InviteToChannelRequest(channel=group, users=[user]))
        print("    → Invited second user")

        # Send 5 image messages
        for i in range(5):
            await client.send_file(group, image_path, caption=image_caption)
            await asyncio.sleep(1)
        print("    → Sent 5 images")

        # Send 5 text messages
        for _ in range(5):
            await client.send_message(group, random.choice(random_messages))
            await asyncio.sleep(1)
        print("    → Sent 5 text messages")

    except Exception as e:
        print(f"[!] Error in group: {e}")

async def main():
    await client.start()
    for x in range(2):
        await create_group()

with client:
    client.loop.run_until_complete(main())
