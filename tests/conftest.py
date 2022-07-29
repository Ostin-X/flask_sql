from src.course_sql.models.models import *
from src.course_sql.app import create_app
from src.course_sql.create_db import create_db,  add_courses, add_students_and_courses_list
import pytest
from src.course_sql.extensions.extensions import app, db, db_test_location


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_test_location
    app.config['TESTING'] = True
    TEST_DB_NAME = db_test_location.split('/')[-1]
    create_db(TEST_DB_NAME)
    with app.app_context():
        db.init_app(app)
    #     db.session.add(GroupModel(name='AA-11'))
    #     db.session.add(GroupModel(name='BB-22'))
        db.drop_all()
    #     db.create_all()
    #     db.session.commit()
    with app.test_client() as client:
        yield client

# @pytest.fixture()
# def runner():
#     app = create_app()
#     return app.test_cli_runner()
