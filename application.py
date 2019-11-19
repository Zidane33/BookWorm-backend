from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from .forms import RegisterForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database config
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wscxawtmtqknwv:500660f9d795a48114d654dd906ed720f12db842c371b2239ad21bedd5f8d04f@ec2-174-129-253-45.compute-1.amazonaws.com:5432/d6et227qpa435r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
KEY = 'Cc5azpsc8j0fATmIxBfhDw'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('logged.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.method == "POST":
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
            return render_template('logged.html')
        else:
            flash('wrong password')
    return index()


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if request.form['logout'] == 'logout':
            session['logged_in'] = False
            return index()

from .model import User


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    app.logger.debug(form.errors)
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('CONGRATS YOU ARE REGISTERED')
    return render_template('register.html', form=form)
