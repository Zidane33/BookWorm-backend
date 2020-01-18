from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os


app = Flask(__name__)
login = LoginManager(app)

# database config
app.config['SECRET_KEY'] = (os.environ['SECRET'])
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ['DATABASE_URL'])
app.config['PASSWORD'] = (os.environ['PASSWORD'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, model
