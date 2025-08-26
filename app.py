from flask import Flask, request
import os
from services.whatsapp_service import send_text_message
from services.langgraph_service import get_intent
from modules.responder import build_response

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        try:
            change = data["entry"][0]["changes"][0]["value"]

            if "messages" in change:
                message = change["messages"][0]
                sender = message["from"]
                text = message.get("text", {}).get("body", "")

                # 🔹 LangGraph intent classification (HF zero-shot)
                intent = get_intent(text)
                response_text = build_response(intent, text)

                send_text_message(sender, response_text)

            elif "statuses" in change:
                status = change["statuses"][0]
                print(f"📬 Status update: {status}")

            else:
                print("⚠️ Unknown webhook event:", change)

        except Exception as e:
            print("❌ Error handling webhook:", str(e))

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))