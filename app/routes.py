from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_session import Session
from flask_login import current_user, login_user, logout_user
import re
from .forms import RegisterForm, LoginForm
from app import app, db
from .model import User, Project, Books
from .api import api, search, searchCite
from .db_methods import addProjectToDatabase


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
        session['user_id'] = user.id
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
    data = zip(bookTitles, links)
    return render_template('search.html', data=data)


@app.route('/project', methods=["POST"])
def add_project():
    userId = session['user_id']
    project = request.form['addProject']
    addProjectToDatabase(project, userId)
    return render_template('dashboard.html')


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
