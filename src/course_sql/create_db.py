from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from src.course_sql.extensions.extensions import app, db
from src.course_sql.models.models import GroupModel, StudentModel, CourseModel
import random
from string import ascii_uppercase

courses_name_list = {'math', 'chemistry', 'physics', 'history', 'biology', 'literature', 'swine-dog hating',
                     'musicology', 'basketball', 'driving'}

first_names = ['Andriy', 'Vadym', 'Oleksander', 'Bohdan', 'Boryslav', 'Danilo', 'Georgiy', 'Kyrylo', 'Marko',
               'Mykhailo', 'Mykola', 'Mykyta', 'Pavlo', 'Petro', 'Pylyp', 'Symon', 'Taras', 'Vasyl', 'Volodymyr',
               'Oleksiy']
last_names = ['Melnyk', 'Shevchenko', 'Bondarenko', 'Kovalenko', 'Boiko', 'Tkachenko', 'Kravchenko', 'Kovalchuk',
              'Koval', 'Shevchuk', 'Polyshchuk', 'Bondar', 'Olyinyk', 'Lysenko', 'Moroz', 'Marchenko', 'Tkachuk',
              'Savchenko', 'Rudenko', 'Petrenko']


def create_db():
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        engine = create_engine(f"postgresql://{app.config['USER']}:{app.config['PASSWD']}@localhost")
        conn = engine.connect()
        conn.execute("commit")
        conn.execute(f"CREATE DATABASE {app.config['SRV']}")


def add_groups():
    group_len = len(GroupModel.query.all())
    while group_len < 10:
        add_group_name = random.choice(ascii_uppercase) + random.choice(ascii_uppercase) + '-' + str(
            random.randint(1, 99))
        db.session.add(GroupModel(name=add_group_name))
        group_len += 1


def add_courses(courses_name_list):
    courses_exist = {course.name for course in CourseModel.query.all()}
    courses_name_list = courses_name_list - courses_exist
    for course_name in courses_name_list:
        course_object = CourseModel(name=course_name, description=course_name + ' - description here')
        db.session.add(course_object)


def add_students_and_courses_list(first_names, last_names):
    student_len = len(StudentModel.query.all())
    courses_query = CourseModel.query.all()
    group_ids = [id[0] for id in GroupModel.query.with_entities(GroupModel.id).all()]
    while student_len < 200:
        student_object = StudentModel(group_id=random.choice(group_ids), first_name=random.choice(first_names),
                                      last_name=random.choice(last_names))
        db.session.add(student_object)

        courses_to_study = random.sample(courses_query, random.randint(1, 3))
        student_object.courses.extend(courses_to_study)

        student_len += 1


def create_sample_data():
    create_db()
    db.create_all()
    add_groups()
    add_courses(courses_name_list)
    add_students_and_courses_list(first_names, last_names)
    db.session.commit()
    print('It is done')


if __name__ == '__main__':
    with app.app_context():
        app.config.from_object('extensions.config.ProdConfig')
        db.init_app(app)
        create_sample_data()
