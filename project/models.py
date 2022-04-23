from flask_login import UserMixin

from project import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# class CardIndex(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # body
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # author = db.Column(db.ForeignKey)
#     # body = db.Column(db.Text)
#     # date = db.Column()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# if __name__ == '__main__':
#     # db.metadata.clear()
#     db.create_all()  # инициализация базы данных
