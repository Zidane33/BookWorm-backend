from flask import session, render_template, request, flash
from flask_session import Session
from .forms import RegisterForm
from app import app, db

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
        elif db.session.query(request.form['password']) and db.session.query(request.form['username']):
            session['logged_in'] = True
            flash('CONGRATS YOU LOGGED IN')
        else:
            flash('wrong password')
    return index()


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        if request.form['logout'] == 'logout':
            session['logged_in'] = False
            return index()


@app.route('/register', methods=['POST', 'GET'])
def register():
    from .model import User
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('CONGRATS YOU ARE REGISTERED')
    return render_template('register.html', form=form)
