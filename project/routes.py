from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy.model import DefaultMeta
from flask_login import current_user

import project
from project import app, db
from project.models import *


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route("/search")
def search():
    if len(request.args) > 0:
        title = request.args.get('title')
        if title is not None:
            _books = BookCard.query.filter_by(title=title)
            return render_template('search_results.html', books=_books)
    else:
        return redirect("/")


@app.route("/account")
def account():
    # проверяем, есть ли у юзера ассоциированная с ним карточка читателя
    user_id = current_user.id
    reader = Reader.query.filter_by(user_id=user_id).first()
    if reader is not None:
        reader_book_cards = ReadersBookCards.query.filter_by(reader_id=reader.id).all()
        books_deadlines = {}
        for item in reader_book_cards:
            books_deadlines[item.bookcard] = item.deadline
        return render_template("account.html", reader=reader, books_deadlines=books_deadlines)
    return render_template("account.html", reader=reader)


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


@app.route("/books", methods=['GET'])
def books():
    _books = BookCard.query.all()
    return render_template('books.html', books=_books)


# TODO: добавить поле количества доступных книг
# TODO: изменять количество книг в соответствии с кол-вом книг отданных и принятых
# TODO: добавить дату возврата книги
