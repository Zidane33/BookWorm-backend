from flask import render_template, flash, redirect, url_for, request, session
from flask_session import Session
from flask_login import current_user, login_user, logout_user, login_required
import re
from .forms import RegisterForm, LoginForm
from app import app, db
from .model import User, Project, Books
from .api import api, search, searchCite
from .db_methods import addProjectToDatabase
from flask_mail import Mail, Message
import os


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Flask-Mail config

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USERNAME='midoz393@gmail.com',
    MAIL_PASSWORD=os.environ['PASSWORD'],
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
))
mail = Mail(app)


# Routes
@app.route("/")
def index():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if 'demoLogin' in request.form:
        demoUser = User.query.filter_by(username='demo').first()
        login_user(demoUser)
        return render_template('dashboard.html')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['user_id'] = user.id
        return render_template('dashboard.html')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    from .model import User
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data,
                 password_hash=form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Congrats, you are registered')
    return render_template('register.html', form=form)


@app.route('/api/', methods=["POST", "GET"])
def api_route():
    projects = Project.query.filter_by(user_id=session['user_id']).all()
    bookId = request.args.get('bookSearch')
    data = api(bookId)
    app.logger.info(data)
    title = data["title"]
    author = data['author']
    description = re.sub('/<.*?>/gm', '', data['description'])
    image = data['image']
    isbn = data['isbn']
    publishDate = data['publishDate']
    return render_template('book.html',
                           title=title,
                           author=author,
                           description=description,
                           image=image,
                           isbn=isbn,
                           publishDate=publishDate,
                           projects=projects)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == 'POST':
        books = Books.query.filter_by(project_id=request.form['project']).all()
        projects = Project.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', projects=projects, books=books)
    projects = Project.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', projects=projects)


@app.route('/search', methods=["GET", "POST"])
def query():
    bookSearch = request.form['bookSearch']
    books = search(bookSearch)
    bookTitles = []
    for title in books['items']:
        bookTitles.append(title['volumeInfo']['title'])
    links = []
    for title in books['items']:
        links.append(title['id'])
    authors = []
    for title in books['items']:
        try:
            authors.append(title['volumeInfo']['authors'][0])
        except KeyError:
            authors.append("Not Found")
    data = zip(bookTitles, links, authors)
    return render_template('search.html', data=data)


@app.route('/project', methods=["POST"])
def add_project():
    userId = session['user_id']
    project = request.form['addProject']
    addProjectToDatabase(project, userId)
    return redirect(url_for('dashboard'))


@app.route('/addBook', methods=["POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        projectId = request.form['project']
        book = Books(title=title, author=author, isbn=isbn, project_id=projectId)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/delete', methods=["POST"])
def delete():
    toDelete = request.form['delete']
    Books.query.filter_by(id=toDelete).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/cite', methods=["POST"])
def cite():
    isbn = request.form['isbnToSearch']
    books = searchCite(isbn)
    bookId = books['items'][0]['id']
    book = api(bookId)
    title = book['title']
    author = book['author'].split()
    firstName = author[0]
    lastName = author[1]
    publishDate = book['publishDate'][:4]
    publisher = book['publisher']
    citation = f"{lastName}, {firstName} ({publishDate}). {title}. {publisher}"
    return render_template('cite.html', citation=citation)


@app.route('/contact', methods=["POST"])
def contact():
    name = request.form['name']
    email = request.form['email']
    msg = request.form['msg']
    sendMsg = Message(subject="bookWorm", reply_to=email, sender=email, recipients=["midoz393@gmail.com"])
    sendMsg.body = 'msg --' + msg + '--name--' + name + '--email--' + email
    mail.send(sendMsg)
    return redirect(url_for('index'))


@app.route('/deleteProject', methods=["POST"])
def deleteProject():
    toDelete = request.form['deleteProject']
    Project.query.filter_by(id=toDelete).delete()
    db.session.commit()
    return redirect(url_for('dashboard'))
