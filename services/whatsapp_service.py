import requests
from config import ACCESS_TOKEN, PHONE_NUMBER_ID

API_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"


def send_text_message(to: str, text: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        print("📨 WhatsApp API:", resp.status_code, resp.text)
    except Exception as e:
        print("❌ WhatsApp send error:", e)