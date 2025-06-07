from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Inicialización global de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Usaremos esto en el siguiente paso

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Importación y registro del blueprint auth (lo crearemos pronto)
    try:
        from .auth import auth as auth_blueprintfrom 
        from . import models
        app.register_blueprint(auth_blueprint)
    except ImportError:
        pass  # Solo si aún no creamos auth.py

    # Ruta base temporal
    @app.route('/')
    def index():
        return "Aplicación funcionando correctamente."

    return app

from . import models