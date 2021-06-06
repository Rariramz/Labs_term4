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
from app import main


data = {
    'url': 'https://f02f159e04ab.ngrok.io'
}
url = 'https://api.telegram.org/botTOKEN/setWebHook'
requests.post(url, data)
