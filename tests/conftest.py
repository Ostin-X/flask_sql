from src.course_sql.models.models import *
from src.course_sql.app import create_app
from src.course_sql.create_db import create_db
import pytest
from src.course_sql.extensions.extensions import app, db


@pytest.fixture(scope='session')
def client():
    app = create_app()
    db_test_location = 'postgresql://postgres:scxscx@localhost/test_coursessql'
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_test_location
    # app.config['TESTING'] = True
    app.config.from_object('src.course_sql.extensions.config.DevConfig')
    TEST_DB_NAME = db_test_location.split('/')[-1]
    create_db(TEST_DB_NAME)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
    with app.test_client() as client:
        yield client

