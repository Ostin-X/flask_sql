from src.course_sql.models.models import *
from src.course_sql.app import create_app
from src.course_sql.create_db import create_db
import pytest
from src.course_sql.extensions.extensions import app, db


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config['TESTING'] = True
    # TEST_DB_NAME = 'test_coursessql'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql:scxscx@localhost/' + TEST_DB_NAME
    # create_db(TEST_DB_NAME)
    # db.create_all()
    # db.session.commit()
    db.init_app(app)
    client = app.test_client()
    yield client

# @pytest.fixture()
# def runner():
#     app = create_app()
#     return app.test_cli_runner()
