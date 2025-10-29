import asyncio
import os
import random
from datetime import datetime
from multiprocessing import Process
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest

# ========= CONFIGURATION =========
try:
    # Environment variables are loaded here.
    api_id_list = list(map(int, os.environ.get("API_IDS", "").split("\n")))
    api_hash_list = os.environ.get("API_HASHS", "").split("\n")
    string_session_list = os.environ.get("STRING_SESSIONS", "").split("\n")
    # Filtering out any empty strings that might result from splitting
    api_id_list = [id for id in api_id_list if id]
    api_hash_list = [h for h in api_hash_list if h]
    string_session_list = [s for s in string_session_list if s]

except Exception as env_error:
    print(f"[!] Failed to load environment variables: {env_error}")
    api_id_list, api_hash_list, string_session_list = [], [], []

second_user_username = 'missrose_bot'
image_path = "screenshot.png"
image_caption = 'Welcome to the group! 🎉'
random_messages = ["Hi", "Hello", "Yo", "What's up?", "How's it going?"]
today = datetime.now().strftime('%Y-%m-%d')

async def create_group(client, group_num):
    """Groups create karne aur content send karne ka main logic."""
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

        # 1. Invite second user
        try:
            user = await client.get_entity(second_user_username)
            await client(InviteToChannelRequest(channel=group, users=[user]))
            print("    → Invited second user")
        except Exception as e:
            print(f"[!] Error inviting user: {e}")

        # 2. Send 5 images
        for _ in range(5):
            try:
                await client.send_file(group, image_path, caption=image_caption)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[!] Error sending image: {e}")
        print("    → Sent 5 images")

        # 3. Send 5 text messages
        for _ in range(5):
            try:
                await client.send_message(group, random.choice(random_messages))
                await asyncio.sleep(1)
            except Exception as e:
                print(f"[!] Error sending message: {e}")
        print("    → Sent 5 text messages")

    except Exception as e:
        print(f"[!] Error in group creation: {e}")

async def run_client(api_id, api_hash, session, sr_number):
    """Telethon client ko initialize aur run karta hai, aur account info print karta hai."""
    try:
        # EDIT: SR number print karna jab account start ho raha hai
        print(f"\n🚀 **Account SR #{sr_number}** is starting to work...")
        
        async with TelegramClient(StringSession(session), api_id, api_hash) as client:
            
            # Account ki details nikalna aur print karna
            try:
                me = await client.get_me()
                name = me.first_name if me.first_name else "N/A"
                username = f"@{me.username}" if me.username else "N/A"
                print(f"\n{'='*50}")
                print(f"🌟 **Starting work with account (SR #{sr_number}):**") # SR number yahan bhi add kar diya
                print(f"  → Name: **{name}**")
                print(f"  → Username: **{username}**")
                print(f"  → API ID: {api_id}")
                print(f"{'='*50}")
            except Exception as e:
                print(f"\n[!] Could not fetch account details for API ID {api_id}. Error: {e}")
                
            # Group creation process starts here.
            for i in range(2):
                await create_group(client, i + 1)
                
    except Exception as e:
        print(f"[!] Client error (API ID {api_id}): {e}")

def start_process(api_id, api_hash, session, sr_number):
    """Har client ke liye ek naya asyncio event loop start karta hai."""
    # EDIT: SR number ko run_client tak pass kiya
    asyncio.run(run_client(api_id, api_hash, session, sr_number))

def main():
    """Main function jo env variables check aur processes start karta hai."""
    
    # **EDIT 1: SAARE Environment Variables ko FULL print karna**
    print("=========================================")
    print("🌍 **Full Environment Variables Loaded:**")
    # os.environ ek dictionary-like object hai, jise hum loop kar sakte hain.
    print(f"TOTAL API_IDS: {len(api_id_list)}")
    print(f"TOTAL API_HASHS: {len(api_hash_list)}")
    print(f"TOTAL STRING_SESSIONS: {len(string_session_list)}")
    print("=========================================\n")


    if not api_id_list or not api_hash_list or not string_session_list:
        print("[!] Environment variables (API_IDS, API_HASHS, STRING_SESSIONS) are missing or incorrectly configured.")
        return

    # Check for misaligned lists (less critical if one is shorter, but good to check)
    min_len = min(len(api_id_list), len(api_hash_list), len(string_session_list))
    if len(api_id_list) != len(api_hash_list) or len(api_hash_list) != len(string_session_list):
        print(f"[!] Warning: Environment lists have unequal lengths! Using the minimum length: {min_len}")
        
    processes = []
    # EDIT 2: enumerate() use kiya SR number (index + 1) nikalne ke liye
    # Zip will stop at the shortest list, which is the safer approach
    for index, (api_id, api_hash, session) in enumerate(zip(api_id_list, api_hash_list, string_session_list)):
        sr_number = index + 1 # SR number 1 se start hoga
        # EDIT 3: sr_number ko start_process mein pass kiya
        p = Process(target=start_process, args=(api_id, api_hash, session, sr_number))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
