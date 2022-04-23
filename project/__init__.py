from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os


os.environ['FLASK_APP'] = 'main'
os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)

app.secret_key = 'CpFQ2zvUg_@Up+6cx&n@sBmmv68U7!WuT3@uvs@!bLsYMHuM4ejP7Z#4%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/redgradient/card-index/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # подавление предупреждения в консоли

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from project.routes import *
from project.models import *

db.create_all()
