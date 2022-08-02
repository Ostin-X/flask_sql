from os import environ, path
from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

load_dotenv()


class Config:
    """Base config."""
    # SECRET_KEY = environ.get('SECRET_KEY')
    # SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    USER = environ.get('USER')
    PASSWD = environ.get('PASSWD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = True
    TESTING = False

    SRV = environ.get('SRV')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{Config.USER}:{Config.PASSWD}@localhost/{SRV}'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = True

    SRV = environ.get('TEST-SRV')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{Config.USER}:{Config.PASSWD}@localhost/{SRV}'
    # SQLALCHEMY_DATABASE_URI = environ.get('TEST_SQLALCHEMY_DATABASE_URI')
