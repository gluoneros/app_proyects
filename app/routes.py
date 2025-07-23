# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Project, List, Card, User
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

@main.route('/project/<int:project_id>')
@login_required
def project_board(project_id):
    project = Project.query.get_or_404(project_id)

    # Verificar que el usuario sea dueño o colaborador
    if project.user_id != current_user.id and current_user not in project.collaborators:
        flash("No tienes acceso a este proyecto.")
        return redirect(url_for('main.dashboard'))

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



@main.route('/project/share/<int:project_id>', methods=['POST'])
@login_required
def share_project(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()

    # Verificar que el usuario sea dueño del proyecto
    if project.user_id != current_user.id:
        flash("No tienes permiso para compartir este proyecto.")
        return redirect(url_for('main.project_board', project_id=project_id))

    email = request.form.get('email')
    user_to_add = User.query.filter_by(email=email).first()

    if not user_to_add:
        flash("No se encontró un usuario con ese correo.")
        return redirect(url_for('main.project_board', project_id=project_id))

    if user_to_add in project.collaborators:
        flash("Este usuario ya es colaborador.")
        return redirect(url_for('main.project_board', project_id=project_id))

    project.collaborators.append(user_to_add)
    db.session.commit()

    flash(f"Usuario {email} ahora puede colaborar en el proyecto.")
    return redirect(url_for('main.project_board', project_id=project_id))