# from os import environ, path
# from dotenv import load_dotenv
#
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    # SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = True
    TESTING = False

    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'postgresql://ASP:qwe@localhost/coursessql'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://ASP:qwe@localhost/test_coursessql'
