from flask_restful import Resource, Api, reqparse
from flask import request, Blueprint
from src.course_sql.db.models import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

parser = reqparse.RequestParser()


class StudentsApi(Resource):
    def get(self):
        result = []
        students_number = request.args.get('students_number')
        if students_number:
            for group in db.session.query(GroupModel).join(StudentModel).group_by(GroupModel).having(
                    db.func.count(GroupModel.students) <= students_number).all():
                result.append({group.name: len(group.students)})
        else:
            result = 'You Get What You Give'
        return result

    def post(self):
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        first_name = parser.parse_args()['first_name']
        last_name = parser.parse_args()['last_name']
        if first_name and last_name:
            student_object = StudentModel(first_name=parser.parse_args()['first_name'],
                                          last_name=parser.parse_args()['last_name'])
            db.session.add(student_object)
            db.session.commit()
            result = f'New poor soul {student_object.first_name} {student_object.last_name} is condemned'
        return result

    def put(self, student_id):
        parser.add_argument('course', type=int, required=True)
        parser.add_argument('course_remove', type=int)
        student_object = StudentModel.query.filter_by(id=student_id).first()
        if parser.parse_args()['course']:
            if len(student_object.courses) > 2:
                result = f'Poor soul {student_object.first_name} {student_object.last_name} is suffering enough'
            course_object = CourseModel.query.filter_by(id=parser.parse_args()['course']).first()
            if course_object in student_object.courses:
                result = f'Poor soul {student_object.first_name} {student_object.last_name} already cursed with {course_object.name}'
            else:
                student_object.courses.append(course_object)
                db.session.commit()
                result = f'Poor soul {student_object.first_name} {student_object.last_name} now cursed with {course_object.name}'
        elif parser.parse_args()['course_remove']:
            course_object = CourseModel.query.filter_by(id=parser.parse_args()['course_remove']).first()
            if course_object in student_object.courses:
                student_object.courses.remove(course_object)
                db.session.commit()
                result = f'Poor soul {student_object.first_name} {student_object.last_name} will suffer {course_object.name} no more'
            else:
                result = f'Poor soul {student_object.first_name} {student_object.last_name} already free from {course_object.name}'
        else:
            result = 'Be wise with your wishes'
        return result

    def delete(self, student_id):
        student_object = StudentModel.query.filter_by(id=student_id).first()
        if student_object:
            db.session.delete(student_object)
            db.session.commit()
            result = f'Good Kill. Number {student_id} is no more. {StudentModel.query.count()} poor bastards to go'
        else:
            result = f'Wrong target mark {student_id}'
        return result


class GroupsApi(Resource):
    def get(self):
        result = []
        group_name = request.args.get('group_name')
        if group_name:
            group_object = GroupModel.query.filter_by(name=group_name).first()
            if group_object:
                for student in group_object.students:
                    result.append(f'{student.first_name} {student.last_name}')
        else:
            result = f'Wrong gathering name {group_name}'
        return result


api.add_resource(StudentsApi, '/students', '/students/<student_id>')
api.add_resource(GroupsApi, '/groups')
