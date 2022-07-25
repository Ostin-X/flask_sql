from flask_restful import Resource, Api
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
            for student in GroupModel.query.filter(GroupModel.name == args('group_name')).first().students:
                result.append(f'{student.first_name} {student.last_name}')
        return result


api.add_resource(GroupApi, '/group')
