from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database config
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wscxawtmtqknwv:500660f9d795a48114d654dd906ed720f12db842c371b2239ad21bedd5f8d04f@ec2-174-129-253-45.compute-1.amazonaws.com:5432/d6et227qpa435r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
KEY = 'Cc5azpsc8j0fATmIxBfhDw'

from app import routes, model
