from src.course_sql.models.models import *
from src.course_sql.app import create_app
from src.course_sql.create_db import create_db
import pytest
from src.course_sql.extensions.extensions import app, db


@pytest.fixture(scope='session')
def client():
    app = create_app()
    app.config.from_object('src.course_sql.extensions.config.DevConfig')
    create_db()
    db.init_app(app)
    with app.app_context():
        db.drop_all()
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def db_create():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        for i in range(2):
            i = str(i)
            db.session.add(GroupModel(id=i, name='AA-' + i * 2))
            db.session.add(CourseModel(id=i, name='course_name_' + i, description='test - description here'))
            for j in range((int(i) + 1) * 3):
                db.session.add(StudentModel(group_id=int(i), first_name='Student_' + str(j),
                                            last_name='Student_' + str(j)))
        db.session.commit()
