"""App configuration."""
from os import environ


class Config:
    """Set Flask configuration vars from environment variables."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    # Uploads
    UPLOADS_DEFAULT_DEST = './app/static/img/'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/'

    UPLOADED_PHOTOS_DEST = './app/static/img/'
    UPLOADED_PHOTOS_URL = 'http://localhost:5000/static/img/'

    # enables the Cross-Site Request Forgery (CSRF) protection in your forms
    WTF_CSRF_ENABLED = True
