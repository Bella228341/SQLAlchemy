from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Users, Roles
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = Roles.query.filter_by(name='guest').first()

        if Users.query.filter_by(username=username).first():
            flash('Username is already taken')
            return redirect(url_for('register'))
        if Users.query.filter_by(email=email).first():
            flash('Email is already taken')
            return redirect(url_for('register'))

        user = Users(username=username, email=email, password=generate_password_hash(password), role_id=role.id)
        db.session.add(user)
        db.session.commit()

        flash('You have been registered!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember)
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
