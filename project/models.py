from flask_login import UserMixin
from sqlalchemy.sql import func

from project import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_staff = db.Column(db.Boolean, default=False)

    # метод __repr__ возвращает строковое представление экземпляра User'a
    # строковые представления используются в админ-панели, чтобы выводить читабельные наименования
    def __repr__(self):
        return f'{self.username}'


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schoolyear = db.Column(db.Integer)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    year_of_birth = db.Column(db.Integer)
    grade = db.Column(db.String(3), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'{self.firstname} {self.lastname}'


class BookCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)
    publishing_year = db.Column(db.Integer)
    description = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'{self.title}, {self.author}'


class ReadersBookCards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=False)
    reader = db.relationship('Reader')
    bookcard_id = db.Column(db.Integer, db.ForeignKey('book_card.id'), nullable=False)
    bookcard = db.relationship('BookCard')
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        reader = Reader.query.filter_by(id=self.reader_id).first()
        bookcard = BookCard.query.filter_by(id=self.bookcard_id).first()
        return f'{reader} - {bookcard}'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User')
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'{self.title}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
