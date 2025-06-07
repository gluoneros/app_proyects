from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

# Login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')

# Registro
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('El nombre de usuario o el correo ya están registrados.')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registro exitoso. Inicia sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
