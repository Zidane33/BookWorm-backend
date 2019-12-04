from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(65), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    projects = db.relationship('Project', backref="User", lazy=True)

    def __repr__(self):
        return '<User {}'.format(self.username)

    def check_password(self, password):
        return self.password_hash == password


class Project(db.Model):
    __tablename__ = 'Projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    books = db.relationship('Books', backref="Project", lazy=True)


class Books(db.Model):
    __tableame = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20))
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
