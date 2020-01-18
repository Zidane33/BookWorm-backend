from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from boto.s3.connection import S3Connection
import os


app = Flask(__name__)
login = LoginManager(app)

# database config
app.config['SECRET_KEY'] = S3Connection(os.environ['SECRET'])
app.config['SQLALCHEMY_DATABASE_URI'] = S3Connection(os.environ['DATABASE_URL'])
app.config['PASSWORD'] = S3Connection(os.environ['PASSWORD'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, model
