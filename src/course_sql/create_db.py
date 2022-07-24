from src.course_sql.config import app, db
from src.course_sql.db.models import GroupModel, StudentModel, CourseModel, student_course_association
import random
from string import ascii_uppercase

db.create_all()

group_len = len(GroupModel.query.all())
while group_len < 10:
    add_name = random.choice(ascii_uppercase) + random.choice(ascii_uppercase) + '-' + str(random.randint(1, 99))
    db.session.add(GroupModel(name=add_name))
    group_len += 1
db.session.commit()

courses_name_list = {'math', 'chemistry', 'physics', 'history', 'biology', 'literature', 'swine-dog hating',
                     'musicology', 'basketball', 'driving'}

courses_exist = {course.name for course in CourseModel.query.all()}
courses_name_list = courses_name_list - courses_exist
for course in courses_name_list:
    db.session.add(CourseModel(name=course, description=course + ' - description here'))
db.session.commit()

first_names = ['Andriy', 'Vadym', 'Oleksander', 'Bohdan', 'Boryslav', 'Danilo', 'Georgiy', 'Kyrylo', 'Marko',
               'Mykhailo', 'Mykola', 'Mykyta', 'Pavlo', 'Petro', 'Pylyp', 'Symon', 'Taras', 'Vasyl', 'Volodymyr',
               'Oleksiy']
last_names = ['Melnyk', 'Shevchenko', 'Bondarenko', 'Kovalenko', 'Boiko', 'Tkachenko', 'Kravchenko', 'Kovalchuk',
              'Koval', 'Shevchuk', 'Polyshchuk', 'Bondar', 'Olyinyk', 'Lysenko', 'Moroz', 'Marchenko', 'Tkachuk',
              'Savchenko', 'Rudenko', 'Petrenko']

student_len = len(StudentModel.query.all())
cour = CourseModel.query.all()
while student_len < 200:
    stud = StudentModel(group_id=random.randint(1, 10), first_name=random.choice(first_names),
                        last_name=random.choice(last_names))
    db.session.add(stud)
    courses_list = []
    for number_of_courses in range(random.randint(1, 3)):
        course_num = random.randint(0, 9)
        while course_num in courses_list:
            course_num = random.randint(0, 9)
        stud.studying.append(cour[course_num])
        courses_list.append(course_num)
    student_len += 1
db.session.commit()

db.session.close()
if __name__ == '__main__':
    app.run(debug=True)
