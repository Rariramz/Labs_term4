from flask import Flask
import requests
from app.config import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app.models import *


data = {
    'url': BOT_URL
}
url = f'{TELEGRAM_URL}/bot{TELEGRAM_BOT_TOKEN}/setWebHook'
requests.post(url, data)

