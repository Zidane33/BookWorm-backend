from flask import render_template, flash, redirect, url_for
from flask_session import Session
from flask_login import current_user, login_user, logout_user
import re
from .forms import RegisterForm, LoginForm
from app import app, db
from .model import User
from .api import api


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return render_template('dashboard.html')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return index()


@app.route('/register', methods=['POST', 'GET'])
def register():
    from .model import User
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data,
                 password_hash=form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('CONGRATS YOU ARE REGISTERED')
    return render_template('register.html', form=form)


@app.route('/api', methods=["GET"])
def api_route():
    data = api()
    title = data["title"]
    author = data['author']
    categories = data['categories']
    description = re.sub('/<.*?>/gm', '', data['description'])
    image = data['image']
    isbn = data['isbn']
    publishDate = data['publishDate']
    return render_template('book.html',
                           title=title,
                           author=author,
                           categories=categories,
                           description=description,
                           image=image,
                           isbn=isbn,
                           publishDate=publishDate)


@app.route('/dashboard', methods=["GET"])
def dashboard():
    return render_template('dashboard.html')
