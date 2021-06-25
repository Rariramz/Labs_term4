import os


TELEGRAM_BOT_TOKEN = os.getenv("telegram_bot_token", default="1840899044:AAF-X6uFxN6oyzFghj0Ub9YXDeuB-vgxWLM")
TELEGRAM_URL = "https://api.telegram.org"
BOT_URL = os.getenv("bot_url", default="https://f737d35910a1.ngrok.io")
BACKEND_URL = os.getenv("backend_url", default="http://0.0.0.0:8000")
