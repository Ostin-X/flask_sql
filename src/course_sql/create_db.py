from src.course_sql.config import app, db
from src.course_sql.db.models import GroupModel, StudentModel, CourseModel
import random
from string import ascii_uppercase
from faker import Faker

fake = Faker()

courses_name_list = {'math', 'chemistry', 'physics', 'history', 'biology', 'literature', 'swine-dog hating',
                     'musicology', 'basketball', 'driving'}

first_names = ['Andriy', 'Vadym', 'Oleksander', 'Bohdan', 'Boryslav', 'Danilo', 'Georgiy', 'Kyrylo', 'Marko',
               'Mykhailo', 'Mykola', 'Mykyta', 'Pavlo', 'Petro', 'Pylyp', 'Symon', 'Taras', 'Vasyl', 'Volodymyr',
               'Oleksiy']
last_names = ['Melnyk', 'Shevchenko', 'Bondarenko', 'Kovalenko', 'Boiko', 'Tkachenko', 'Kravchenko', 'Kovalchuk',
              'Koval', 'Shevchuk', 'Polyshchuk', 'Bondar', 'Olyinyk', 'Lysenko', 'Moroz', 'Marchenko', 'Tkachuk',
              'Savchenko', 'Rudenko', 'Petrenko']


def add_groups():
    group_len = len(GroupModel.query.all())
    while group_len < 10:
        add_name = random.choice(ascii_uppercase) + random.choice(ascii_uppercase) + '-' + str(random.randint(1, 99))
        db.session.add(GroupModel(name=add_name))
        group_len += 1


def add_courses(courses_name_list):
    courses_exist = {course.name for course in CourseModel.query.all()}
    courses_name_list = courses_name_list - courses_exist
    for course_name in courses_name_list:
        course = CourseModel(name=course_name, description=course_name + ' - description here')
        db.session.add(course)


def add_students_and_courses_list(first_names, last_names):
    student_len = len(StudentModel.query.all())
    courses_query = CourseModel.query.all()
    while student_len < 200:
        student = StudentModel(group_model_id=random.randint(1, 10), first_name=random.choice(first_names),
                               last_name=random.choice(last_names))
        db.session.add(student)

        courses_to_study = random.sample(courses_query, random.randint(1, 3))
        student.courses.extend(courses_to_study)

        student_len += 1


def create_sample_data():
    db.create_all()
    add_groups()
    add_courses(courses_name_list)
    add_students_and_courses_list(first_names, last_names)


create_sample_data()
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
