from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from models import User
from __init__ import db

auth = Blueprint('auth', __name__)

@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return render_template('dashboard.html')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists :(')
            return redirect(url_for('auth.register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful, please log in ;D')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return render_template('dashboard.html')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return render_template('dashboard.html')
        flash('Wrong username or password. I cannot tell you which one is wrong.')
    return render_template('login.html')

@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    #originally url_for index
    return render_template('index.html')