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


async def create_group(client, group_num):
    try:
        title = f"{today} Group {group_num}"
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


async def run_for_account(api_id, api_hash, string_session, index):
    try:
        async with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
            print(f"\n[Account {index+1}] Logged in")
            for i in range(2):  # Create 2 groups per account
                await create_group(client, i + 1)
                await asyncio.sleep(2)  # Delay between groups to avoid rate limiting
    except Exception as e:
        print(f"[!] Client session error (account {index+1}): {e}")


async def main():
    if not api_id_list or not api_hash_list or not string_session_list:
        print("[!] Skipping run because environment variables are missing or empty.")
        return

    tasks = []
    for i, (api_id, api_hash, session) in enumerate(zip(api_id_list, api_hash_list, string_session_list)):
        tasks.append(run_for_account(api_id, api_hash, session, i))

    await asyncio.gather(*tasks)


try:
    asyncio.run(main())
except Exception as e:
    print(f"[!] Fatal error in asyncio loop: {e}")
