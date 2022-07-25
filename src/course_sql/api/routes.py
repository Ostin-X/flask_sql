from flask_restful import Resource, Api, reqparse
from flask import request, Blueprint
from src.course_sql.db.models import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)
parser.add_argument('course', type=int)
parser.add_argument('course_remove', type=int)


class GroupApi(Resource):
    def get(self):
        result = []
        args = request.args.get
        if args('students_number'):
            for group in db.session.query(GroupModel).join(StudentModel).group_by(GroupModel).having(
                    db.func.count(GroupModel.students) <= args('students_number')).all():
                result.append(f'{group.name} {len(group.students)}')
        elif args('group_name'):
            group_object = GroupModel.query.filter_by(name=args('group_name')).first()
            if group_object:
                for student in group_object.students:
                    result.append(f'{student.first_name} {student.last_name}')
            else:
                result = f'Wrong gathering name {args("group_name")}'
        return result

    def post(self):
        student_object = StudentModel(first_name=parser.parse_args()['first_name'],
                                      last_name=parser.parse_args()['last_name'])
        db.session.add(student_object)
        db.session.commit()
        return f'New poor soul {parser.parse_args().values()} is condemned'

    def put(self, student_id):
        student_object = StudentModel.query.filter_by(id=student_id).first()
        if parser.parse_args()['course']:
            if len(student_object.courses) > 2:
                result = f'Poor soul {student_object.first_name} {student_object.last_name} is suffering enough'
            course_object = CourseModel.query.filter_by(id=parser.parse_args()['course']).first()
            if course_object in student_object.courses:
                result = f'Poor soul {student_object.first_name} {student_object.last_name} already cursed with {course_object.name}'
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
                result = f'Poor soul {student_object.first_name} {student_object.last_name} is free from {course_object.name}'
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


api.add_resource(GroupApi, '/group', '/group/<student_id>')
