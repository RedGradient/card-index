from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_perm import Perm
from flask_migrate import Migrate
from flask_admin.menu import MenuLink


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

"""
Миграции позволяют добавлять новые столбцы и таблицы в базу данных, не пересоздавая ее заново.
Использование:
Инициализация репозитория (выполняется один раз):
    python3 -m flask db init
После каждого изменения базы данных нужно выполнить команды:
    python3 -m flask db migrate -m "Initial migration."
    python3 -m flask db upgrade
"""
migrate = Migrate(app, db)

login_manager = LoginManager(app)


from project.routes import *
from project.models import *

# создаем админ-панель
admin = Admin(app)

# для удобства добавляем в админ-панель ссылку на главную страницу
admin.add_link(MenuLink(name='Вернуться на главную страницу', url='/'))

# добавляем поддержку прав доступа
perm = Perm(app)


# регистрируем загрузчик пользователя (необходимо для работы Flask-Perm)
@perm.current_user_loader
def load_current_user():
    return current_user


class MyModelView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created',)


# добавляем наши модели в админ-панель
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Reader, db.session))
admin.add_view(MyModelView(BookCard, db.session))
admin.add_view(MyModelView(ReadersBookCards, db.session))
admin.add_view(MyModelView(Post, db.session))

# создаем базу данных, если ее нет
db.create_all()

# создаем суперпользователя, если его нет
staff = User.query.filter_by(is_staff=True)
if len(list(staff)) == 0:
    superuser = User(username='admin', password='admin', email='example@mail.com', is_staff=True)
    db.session.add(superuser)
    db.session.commit()
