import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .variables import KEY
import requests

app = Flask(__name__)
os.environ['DATABASE_URL'] = 'postgres://wscxawtmtqknwv:500660f9d795a48114d654dd906ed720f12db842c371b2239ad21bedd5f8d04f@ec2-174-129-253-45.compute-1.amazonaws.com:5432/d6et227qpa435r'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/") #look at the goodreads api methods
def index(): 
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "08223716321681460840"})
    return print(res.json())
