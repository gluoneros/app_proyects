from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from flask_login import login_required, current_user

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
    # Aquí deberías llamar a tu función de registro real
    return render_template('register.html')

@main.route('/logout')
def logout_route():
    # Aquí deberías llamar a tu función de logout real
    return "Logout"

@main.route('/dashboard')
@login_required
def dashboard():
    return f"Bienvenido, {current_user.username}. Estás en el panel de control."