from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required

import project
from project import app, db
from project.models import *


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        # если пароли совпадают
        if username and password:
            # получаем пользователя с совпадающим username
            user = User.query.filter_by(username=username).first()

            if (user is not None and
                    user.password == password):
                login_user(user)  # авторизация
                return redirect('/')  # перенаправление на домашнюю страницу
            else:
                flash('Неверный пароль')
        else:
            flash('Необходимо заполнить все поля')

        return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/register", methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        if not (username or password or email):
            flash('Необходимо заполнить все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            # создаем нового пользователя
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

        print(username, password)
        return render_template('register.html')


@app.route("/admin", methods=['GET'], defaults={'model_name': None})
@app.route("/admin/<model_name>", methods=['GET'])
# @login_required
def admin(model_name):
    if model_name is None:
        return render_template('admin.html',
                               users=User.__tablename__,
                               readers=Reader.__tablename__,
                               book_cards=BookCard.__tablename__,
                               reader_bookcard=Reader_BookCard.__tablename__)
    else:
        # ищем модель по названию таблицы
        for model in dir(project.models):
            cls = getattr(project.models, model)
            if cls.__tablename__ == model_name:
                return render_template('model_content.html', content=cls().query.all())

        return f'<h1>Таблица {model_name} не найдена</h1>'
