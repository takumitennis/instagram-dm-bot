
from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route('/')
def index():
    return "Instagram DM Bot is running!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Invalid verification token', 403

    if request.method == 'POST':
        data = request.get_json()
        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging['sender']['id']
                if 'message' in messaging:
                    message_text = messaging['message'].get('text', '').lower()
                    if '応募' in message_text:
                        send_dm(sender_id)
        return 'ok', 200

def send_dm(sender_id):
    message = {
        "recipient": {"id": sender_id},
        "message": {
            "text": "ご応募ありがとうございます🙇‍♂️\n詳細確認のため、以下のLINEを追加してください📱\n▶️ https://lin.ee/your-line-link"
        }
    }
    response = requests.post(
        f"https://graph.facebook.com/v18.0/me/messages?access_token={ACCESS_TOKEN}",
        json=message
    )
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
