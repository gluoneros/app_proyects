from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Project
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

@main.route('/project/create', methods=['POST'])
@login_required
def create_project():
    name = request.form.get('name')
    description = request.form.get('description')

    new_project = Project(name=name, description=description, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()

    flash('Proyecto creado correctamente.')
    return redirect(url_for('main.dashboard'))