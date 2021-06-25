from threading import Thread

from app import *
from flask import request


@app.route('/', methods=["POST"])
def home():
    if "message" not in request.json:
        return ""
    user_id = request.json["message"]["from"]["id"]

    try:
        message = request.json["message"]["text"]
    except KeyError as e:
        send_messages_to_users([(f"❌ Стикеры не поддерживаются", user_id)])
        return ""

    log(f'Пользователь с ID {user_id} прислал сообщение "{message}"')
    data = {"user_id": user_id, "message": message}
    Thread(target=proceed_message, args=(data,)).start()
    return ""


def proceed_message(data):
    response = requests.post(BACKEND_URL, data=data).json()
    send_messages_to_users(response)


def send_message(message, to_user_id):
    method = "sendMessage"
    token = TELEGRAM_BOT_TOKEN
    url = TELEGRAM_URL
    url = f"{url}/bot{token}/{method}"
    data = {"chat_id": to_user_id, "text": message}
    requests.post(url, data=data)


def send_messages_to_users(messages_to_users):
    for message, user_id in messages_to_users:
        send_message(message, user_id)
        log(f'Сообщение: "{message}" отправлено пользователю с ID {user_id}')


def log(message):
    print(message)


app.run(host="0.0.0.0", port=5000)
