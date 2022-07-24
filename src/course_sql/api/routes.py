from flask_restful import Resource, abort, Api
from flask import request, Response, Blueprint, jsonify
from dict2xml import dict2xml
from src.course_sql.db.models import *

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class GroupApi(Resource):
    def get(self):
        result = {}
        students_number = 21
        # for group in GroupModel.query.all():
        #     if len(group.students) <= students_number:
        #         result[group.name] = len(group.students)
        # result['-------']= '--------------'
        for group in GroupModel.query.all():
            groups_student = StudentModel.query.filter_by(group_model_id=group.id).all()
            for student in groups_student:
                # result[str(student.first_name)+' '+str(student.last_name)] = group.name
                if group.name in result:
                    result[group.name].append(student.first_name + ' ' + student.last_name)
                else:
                    result[group.name] = []
        group = GroupModel.query.filter(GroupModel.students.is_(None)).all()
        for g in group:
            print(g)

        return result


api.add_resource(GroupApi, '/group')
