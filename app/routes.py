from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Project
from app import db

main = Blueprint('main', __name__)

@main.route('/') # Ruta principal
def index():
    return render_template('index.html')

@main.route('/dashboard') # Ruta del dashboard
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects)

@main.route('/project/create', methods=['POST']) # Ruta para crear un proyecto
@login_required
def create_project():
    name = request.form.get('name')
    description = request.form.get('description')

    new_project = Project(name=name, description=description, user_id=current_user.id)
    db.session.add(new_project)
    db.session.commit()

    flash('Proyecto creado correctamente.')
    return redirect(url_for('main.dashboard'))

@main.route('/project/<int:project_id>') # Ruta para ver el tablero de un proyecto
@login_required
def project_board(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    return render_template('project_board.html', project=project)

# app/routes.py

@main.route('/list/create/<int:project_id>', methods=['POST'])
@login_required
def create_list(project_id):
    title = request.form.get('title')
    new_list = List(title=title, project_id=project_id)
    db.session.add(new_list)
    db.session.commit()
    flash('Lista creada correctamente.')
    return redirect(url_for('main.project_board', project_id=project_id))


@main.route('/card/create/<int:list_id>', methods=['POST'])
@login_required
def create_card(list_id):
    title = request.form.get('title')
    description = request.form.get('description')
    new_card = Card(title=title, description=description, list_id=list_id)
    db.session.add(new_card)
    db.session.commit()
    flash('Tarjeta creada correctamente.')
    return redirect(url_for('main.project_board', project_id=new_card.list.project_id))

@main.route('/project/<int:project_id>')
@login_required
def project_board(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    return render_template('project_board.html', project=project)