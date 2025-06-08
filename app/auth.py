from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import main

from app import db
from app.models import User

# Login
#@app.route('/login', methods=['GET', 'POST']) # Definimos la ruta para el inicio de sesión
def login(): # definimos la función login
    if request.method == 'POST': # Verificamos si el método de la solicitud es POST
        username = request.form['username'] # Obtenemos el nombre de usuario del formulario
#        email = request.form.get('email')
        password = request.form['password']
        user = User.query.filter_by(username=username).first() # Buscamos el usuario en la base de datos por nombre de usuario

        if user and user.check_password(password): # Verificamos si el usuario existe y si la contraseña es correcta
            login_user(user)
            return redirect(url_for('dashboard'))
        else: # Si el usuario no existe o la contraseña es incorrecta
            flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html') # Renderizamos la plantilla de inicio de sesión

# Registro
def register():
    if request.method == 'POST': # Verificamos si el método de la solicitud es POST
        username = request.form['username'] # Obtenemos el nombre de usuario del formulario
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
