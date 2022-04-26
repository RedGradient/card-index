from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# устанавливаем переменные окружения, чтобы запустить сервер в development режиме
os.environ['FLASK_APP'] = 'main'
os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)

app.secret_key = 'CpFQ2zvUg_@Up+6cx&n@sBmmv68U7!WuT3@uvs@!bLsYMHuM4ejP7Z#4%'

full_path = os.path.normpath(__file__)  # полный путь к этому файлу (к __init__.py)
parent = os.path.dirname(full_path)  # полный путь к директории, в которой находится __init__.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{parent}/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # подавление предупреждения в консоли

db = SQLAlchemy(app)  # объект базы данных
login_manager = LoginManager(app)


from project.routes import *
from project.models import *

# создаем админ-панель
admin = Admin(app)

# добавляем наши модели в админ-панель
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Reader, db.session))
admin.add_view(ModelView(BookCard, db.session))
admin.add_view(ModelView(ReadersBookCards, db.session))
admin.add_view(ModelView(Post, db.session))

# создаем базу данных, если ее нет
db.create_all()
