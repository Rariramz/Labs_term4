import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = f"postgresql://admin:admin@bot-db/illuminatenorden"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


TELEGRAM_BOT_TOKEN = os.getenv("telegram_bot_token")
TELEGRAM_URL = "https://api.telegram.org"
BOT_URL = os.getenv("bot_url")
