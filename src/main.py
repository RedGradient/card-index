import os
from flask import Flask, render_template, request
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        return render_template('login.html')


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        return render_template('registration')


if __name__ == '__main__':
    os.environ['FLASK_APP'] = 'main'
    os.environ['FLASK_ENV'] = 'development'

    app.run()
