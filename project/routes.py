from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy.model import DefaultMeta

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
def register():
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


def get_model_by_name(model_name):
    # ищем класс модели по имени таблицы
    for model in dir(project.models):
        obj = getattr(project.models, model)
        if isinstance(obj, DefaultMeta) and obj.__tablename__ == model_name:
            return obj
    return None
