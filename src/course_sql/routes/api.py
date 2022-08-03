from flask_restful import Resource, Api, reqparse, abort
from flask import request, Blueprint

from src.course_sql.models.models import StudentModel, GroupModel, CourseModel, db

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

parser = reqparse.RequestParser()


class StudentsApi(Resource):

    def get(self):
        result = []
        students_number = request.args.get('students_number')
        students_in_group_count = db.func.count(GroupModel.students)

        if students_number:
            # for group in db.session.query(GroupModel).join(StudentModel).group_by(GroupModel).having(
            #         db.func.count(GroupModel.students) <= students_number).all():
            for group in GroupModel.query.join(StudentModel).group_by(GroupModel).having(
                    students_in_group_count <= students_number).order_by(students_in_group_count).all():
                result.append({group.name: len(group.students)})
        else:
            abort(400, message='You Get What You Give')

        return {'data': result}, 200

    def post(self):
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        args = parser.parse_args()

        first_name = args['first_name']
        last_name = args['last_name']
        student_object = StudentModel(first_name=first_name, last_name=last_name)

        db.session.add(student_object)
        db.session.commit()

        result = {'id': student_object.id, 'first_name': first_name, 'last_name': last_name}

        return {'data': result}, 201

    def delete(self, student_id):
        student_object = StudentModel.query.get(student_id)

        if student_object:
            db.session.delete(student_object)
        else:
            abort(404, message='Bastard is missing')

        db.session.commit()

        return '', 204


class StudentsCourses(Resource):

    def put(self, student_id):
        parser.add_argument('course', type=int)
        args = parser.parse_args()

        course_add = args['course']

        student_object = StudentModel.query.get(student_id)

        if not student_object:
            abort(400, message=f'Bastard is missing')

        if course_add:
            if len(student_object.courses) > 2:
                abort(400,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} is suffering enough')

            course_object = CourseModel.query.get(course_add)

            if not course_object:
                abort(404, message=f'Wrong sourcery number {course_add}')

            if course_object in student_object.courses:
                abort(400,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} already cursed with {course_object.name}')
            else:
                student_object.courses.append(course_object)
                result = {'id': student_object.id, 'first_name': student_object.first_name,
                          'last_name': student_object.last_name, 'courses': course_object.name}
        else:
            abort(400, message='Be wise with your wishes')

        db.session.commit()

        return {'data': result}, 200

    def delete(self, student_id):
        parser.add_argument('course', type=int)
        args = parser.parse_args()

        course_remove = args['course']
        student_object = StudentModel.query.get(student_id)

        if not student_object:
            abort(404, message=f'Bastard is missing')

        if course_remove:
            course_object = CourseModel.query.get(course_remove)
            if course_object in student_object.courses:
                student_object.courses.remove(course_object)
            else:
                abort(404,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} already free from {course_object.name}')
        else:
            db.session.delete(student_object)

        db.session.commit()

        return '', 204


class CoursesApi(Resource):

    def get(self):

        result = []
        course_name = request.args.get('course_name')

        if course_name:
            course_object = CourseModel.query.filter_by(name=course_name).one_or_none()
            if course_object:
                for student in course_object.students:
                    result.append({'first_name': student.first_name, 'last_name': student.last_name})
            else:
                abort(400, message=f'Wrong sourcery name {course_name}')
        else:
            abort(400, message='You Get What You Give')

        return {'data': result}, 200


api.add_resource(StudentsApi, '/students', '/students/<int:student_id>')
api.add_resource(StudentsCourses, '/students/<int:student_id>/courses')
api.add_resource(CoursesApi, '/courses')
