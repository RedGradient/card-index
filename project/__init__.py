from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


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


admin = Admin(app)

# добавляем модели в админ-панель
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Reader, db.session))
admin.add_view(ModelView(BookCard, db.session))
admin.add_view(ModelView(ReadersBookCards, db.session))
admin.add_view(ModelView(Post, db.session))

db.create_all()
