from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_perm import Perm
# from flask_migrate import Migrate
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
# migrate = Migrate(app, db)

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


class UserView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created',)
    column_searchable_list = ['id', 'username', 'time_created', 'is_staff']
    column_filters = ['id', 'username', 'time_created', 'is_staff']
    page_size = 50


class ReaderView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created', )
    column_searchable_list = ['id', 'user_id', 'schoolyear', 'firstname', 'lastname', 'year_of_birth', 'grade', 'time_created']
    column_filters = ['id', 'user_id', 'schoolyear', 'firstname', 'lastname', 'year_of_birth', 'grade', 'time_created']
    page_size = 50


class BookCardView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created',)
    column_searchable_list = ['id', 'author', 'title', 'publisher', 'publishing_year', 'description']
    column_filters = ['id', 'author', 'title', 'publisher', 'publishing_year', 'description']
    page_size = 50


class ReadersBookCardsView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created',)
    column_searchable_list = ['id', 'reader_id', 'bookcard_id', 'deadline', 'deadline']
    column_filters = ['id', 'reader_id', 'bookcard_id', 'deadline', 'deadline']
    page_size = 50


class PostView(ModelView):
    # поле time_created не будет показываться в админ-панели
    form_excluded_columns = ('time_created',)
    column_searchable_list = ['id', 'author_id', 'title', 'body', 'time_created']
    column_filters = ['id', 'author_id', 'title', 'body', 'time_created']
    page_size = 50


# добавляем наши модели в админ-панель
admin.add_view(UserView(User, db.session))
admin.add_view(ReaderView(Reader, db.session))
admin.add_view(BookCardView(BookCard, db.session))
admin.add_view(ReadersBookCardsView(ReadersBookCards, db.session))
admin.add_view(PostView(Post, db.session))

# создаем базу данных, если ее нет
db.create_all()

# создаем суперпользователя, если его нет
staff = User.query.filter_by(is_staff=True)
if len(list(staff)) == 0:
    superuser = User(username='admin', password='admin', email='example@mail.com', is_staff=True)
    db.session.add(superuser)
    db.session.commit()
