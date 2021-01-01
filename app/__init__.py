from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

app = Flask(__name__)
app.config.from_object('config')
logging.basicConfig(filename='app.log', level=logging.DEBUG)
db = SQLAlchemy(app)
# Handles all migrations.
migrate = Migrate(app, db)

from .models import User

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

from app import views, models
