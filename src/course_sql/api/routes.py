from flask_restful import Resource, Api, reqparse
from flask import request, Blueprint
from src.course_sql.db.models import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class GroupApi(Resource):
    def get(self):
        result = []
        args = request.args.get
        if args('students_number'):
            for group in db.session.query(GroupModel).join(StudentModel).group_by(GroupModel).having(
                    db.func.count(GroupModel.students) <= args('students_number')).all():
                result.append(f'{group.name} {len(group.students)}')
        if args('group_name'):
            group_object = GroupModel.query.filter_by(name=args('group_name')).first()
            if group_object:
                for student in group_object.students:
                    result.append(f'{student.first_name} {student.last_name}')
            else:
                result = f'Wrong group name {args("group_name")}'
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        student = StudentModel(first_name=parser.parse_args()['first_name'], last_name=parser.parse_args()['last_name'])
        db.session.add(student)
        db.session.commit()
        return f'New poor soul {parser.parse_args().values()} cursed'

    def delete(self, student_id):
        student_object = StudentModel.query.filter_by(id=student_id).first()
        if student_object:
            db.session.delete(student_object)
            db.session.commit()
            return f'Good Kill. Number {student_id} is no more. {StudentModel.query.count()} poor bastards to go'
        else:
            return f'Wrong student id {student_id}'


api.add_resource(GroupApi, '/group', '/group/<student_id>')
