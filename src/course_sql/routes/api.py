from flask_restful import Resource, Api, reqparse, abort
from flask import request, Blueprint

from src.course_sql.models.models import StudentModel, GroupModel, CourseModel, db

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class StudentsApi(Resource):
    def get(self):
        result = []
        # students_number = request.args.get('students_number')
        # Тут, напевно, парсер не потрібен. Цікаву цяцьку знайшов))
        # Чи є сенс його так використовувати?
        parser = reqparse.RequestParser()
        parser.add_argument('students_number', location='args')

        students_number = parser.parse_args()['students_number']
        students_in_group_count = db.func.count(GroupModel.students)

        if students_number:
            # for group in db.session.query(GroupModel).join(StudentModel).group_by(GroupModel).having(
            #         db.func.count(GroupModel.students) <= students_number).all():
            for group in GroupModel.query.join(StudentModel).group_by(GroupModel).having(
                    students_in_group_count <= students_number).order_by(students_in_group_count).all():
                result.append({group.name: len(group.students)})
        else:
            abort(400, message='You Get What You Give')

        return result, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)

        first_name = parser.parse_args()['first_name']
        last_name = parser.parse_args()['last_name']
        student_object = StudentModel(first_name=first_name, last_name=last_name)

        db.session.add(student_object)
        db.session.commit()

        result = f'New poor soul {student_object.first_name} {student_object.last_name} is condemned'

        return result, 201

    def put(self, student_id):
        parser = reqparse.RequestParser()
        parser.add_argument('course_add', type=int)
        parser.add_argument('course_remove', type=int)

        course_add = parser.parse_args()['course_add']
        course_remove = parser.parse_args()['course_remove']
        student_object = StudentModel.query.get(student_id)

        if course_add:
            if len(student_object.courses) > 2:
                abort(400,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} is suffering enough')

            course_object = CourseModel.query.get(course_add)

            if course_object in student_object.courses:
                abort(400,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} already cursed with {course_object.name}')
            else:
                student_object.courses.append(course_object)
                result = f'Poor soul {student_object.first_name} {student_object.last_name} now cursed with {course_object.name}'

        elif course_remove:
            course_object = CourseModel.query.get(course_remove)
            if course_object in student_object.courses:
                student_object.courses.remove(course_object)
                result = f'Poor soul {student_object.first_name} {student_object.last_name} will suffer {course_object.name} no more'
            else:
                abort(404,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} already free from {course_object.name}')
        else:
            abort(400, message='Be wise with your wishes')

        db.session.commit()

        return result, 200

    def delete(self, student_id):
        student_object = StudentModel.query.get(student_id)

        if student_object:
            db.session.delete(student_object)
            db.session.commit()
            result = f'Good Kill. Number {student_id} is no more. {StudentModel.query.count()} poor bastards to go'
        else:
            abort(404, message=f'Wrong target mark {student_id}')

        return result, 200


class GroupsApi(Resource):
    def get(self):

        result = []
        group_name = request.args.get('group_name')

        if group_name:
            group_object = GroupModel.query.filter_by(name=group_name).one_or_none()
            if group_object:
                for student in group_object.students:
                    result.append(f'{student.first_name} {student.last_name}')
            else:
                abort(400, message=f'Wrong gathering name {group_name}')
        else:
            abort(400, message='You Get What You Give')

        return result, 200


api.add_resource(StudentsApi, '/students', '/students/<student_id>')
api.add_resource(GroupsApi, '/groups')
