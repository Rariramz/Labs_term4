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
    'url': 'https://90059a42b9b1.ngrok.io'
}
url = 'https://api.telegram.org/botTOKEN/setWebHook'
requests.post(url, data)


# if Group.query.get(1) is None:
#     group = Group(id=1, name="main_chat", admin_id=None)
#     db.session.add(group)
#     db.session.commit()
