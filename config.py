import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://app_proyecs_user:usuario7@localhost:5432/app_proyects')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
