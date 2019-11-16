import os

from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json

app = Flask(__name__)
KEY = 'Cc5azpsc8j0fATmIxBfhDw'


# Check for environment variable
os.environ['DATABASE_URL'] = 'postgres://wscxawtmtqknwv:500660f9d795a48114d654dd906ed720f12db842c371b2239ad21bedd5f8d04f@ec2-174-129-253-45.compute-1.amazonaws.com:5432/d6et227qpa435r'
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": "1632168146"})
    # x = res.json()
    # return x

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('logged.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password')
    return index()

@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if request.form['logout'] == 'logout':
            session['logged_in'] = False
            return index()


