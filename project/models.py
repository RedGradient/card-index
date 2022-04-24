from flask_login import UserMixin
from sqlalchemy.sql import func

from project import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    is_staff = db.Column(db.Boolean, default=False)


class Reader(db.Model):
    __tablename__ = 'Readers'
    id = db.Column(db.Integer, primary_key=True)
    schoolyear = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    year_of_birth = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(3), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


class BookCard(db.Model):
    __tablename__ = 'BookCards'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)
    publishing_year = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), nullable=False)


class Reader_BookCard(db.Model):
    __tablename__ = 'Reader_BookCard'
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('Readers.id'))
    bookcard_id = db.Column(db.Integer, db.ForeignKey('BookCards.id'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


# class Post(db.Model):
#     __tablename__ = 'Posts'
#     id = db.Column(db.Integer, primary_key=True)
#     # author = db.Column(db.ForeignKey)
#     # body = db.Column(db.Text)
#     # time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# if __name__ == '__main__':
#     # db.metadata.clear()
#     db.create_all()  # инициализация базы данных
