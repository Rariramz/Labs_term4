from flask import Flask
import requests
from app.config import *

app = Flask(__name__)

data = {
    'url': BOT_URL
}
url = f'{TELEGRAM_URL}/bot{TELEGRAM_BOT_TOKEN}/setWebHook'
requests.post(url, data)
