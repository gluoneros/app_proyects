from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from flask_login import login_required, current_user
from . import routes

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login_route():
    # Aquí deberías llamar a tu función de login real
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verifica si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('main.register_route'))

        # Crea el usuario y guarda en la base de datos
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.')
        return redirect(url_for('main.login_route'))

    return render_template('register.html')

@main.route('/logout')
def logout_route():
    # Aquí deberías llamar a tu función de logout real
    return "Logout"

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')