import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://usuario:usuario6@localhost:5432/app_proyects')
    #QLALCHEMY_DATABASE_URI = 'postgresql://usuario:contraseña@localhost:5432/nombre_basedatos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
