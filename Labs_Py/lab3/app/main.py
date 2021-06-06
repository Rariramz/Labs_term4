from app import app, db
from flask import request
import requests
from config import *
from app.models import *


@app.route('/', methods=["POST"])
def home():
    user_id = request.json["message"]["from"]["id"]
    user = User.query.get(int(user_id))

    try:
        message = request.json["message"]["text"]
    except ValueError as e:
        send_message("Message is not supported", user_id)
        return ""

    if user is None:
        user = User(id=user_id)
        db.session.add(user)
        db.session.commit()
        send_message("You joined the chat", user_id)
    else:
        send_message(f'hi, {request.json["message"]["from"]["first_name"]}', user_id)
        users = User.query.filter(User.id != int(user_id)).all()
        for user in users:
            send_message(message, user.id)

    return ""


def send_message(message, user_id):
    method = "sendMessage"
    token = TELEGRAM_BOT_TOKEN
    url = TELEGRAM_BOT_URL
    url = f"{url}/bot{token}/{method}"
    data = {"chat_id": user_id, "text": message}
    requests.post(url, data=data)


app.run()
