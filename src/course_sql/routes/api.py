from flask_restful import Resource, Api, reqparse, abort
from flask import request, Blueprint
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from src.course_sql.models.models import StudentModel, GroupModel, CourseModel, db

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

parser_add_student = reqparse.RequestParser()
parser_add_student.add_argument('first_name', type=str, required=True)
parser_add_student.add_argument('last_name', type=str, required=True)

parser_manage_courses = reqparse.RequestParser()
parser_manage_courses.add_argument('course', type=int)


class StudentsApi(Resource):

    def get(self):
        result = []
        students_number = request.args.get('students_number')
        students_in_group_count = db.func.count(GroupModel.students)

        if students_number:
            for group in GroupModel.query.join(StudentModel).group_by(GroupModel).having(
                    students_in_group_count <= students_number).all():
                result.append(group.name)
        else:
            abort(400, message='You Get What You Give')

        return {'data': result}, 200

    def post(self):
        args = parser_add_student.parse_args()

        first_name = args['first_name']
        last_name = args['last_name']
        student_object = StudentModel(first_name=first_name, last_name=last_name)

        db.session.add(student_object)
        db.session.commit()

        result = {'id': student_object.id, 'first_name': first_name, 'last_name': last_name}

        return {'data': result}, 201

    def delete(self, student_id):
        StudentModel.query.filter_by(id=student_id).delete()
        db.session.commit()

        return '', 204


class StudentsCourses(Resource):

    def put(self, student_id):
        args = parser_manage_courses.parse_args()
        course_add = args['course']
        student_object = StudentModel.query.get(student_id)

        if not student_object:
            abort(404, message=f'Bastard is missing')
        if course_add is not None:
            if len(student_object.courses) > 2:
                abort(400,
                      message=f'Poor soul {student_object.first_name} {student_object.last_name} is suffering enough')

            course_object = CourseModel.query.get(course_add)

            if not course_object:
                abort(400, message=f'Wrong sourcery number {course_add}')

            try:
                student_object.courses.append(course_object)
                db.session.commit()
            except IntegrityError as e:
                assert isinstance(e.orig, UniqueViolation)
                db.session.rollback()
            finally:
                courses_list = [course.id for course in student_object.courses]
                result = {'id': student_object.id, 'first_name': student_object.first_name,
                          'last_name': student_object.last_name, 'courses': courses_list}
        else:
            abort(400, message='Be wise with your wishes')

        return {'data': result}, 200

    def delete(self, student_id, course_id):
        student_object = StudentModel.query.get(student_id)

        if not student_object:
            abort(404, message=f'Bastard is missing')

        if course_id is not None:
            course_object = CourseModel.query.get(course_id)

            # ось ця перевірка потрібна? все ще не повністю розумію логіку
            # if not course_object:
            #     abort(400, message=f'Wrong sourcery number {course_id}')

            try:
                student_object.courses.remove(course_object)
            except ValueError:
                db.session.rollback()
            else:
                db.session.commit()
        else:
            abort(400, message='Be wise with your wishes')

        return '', 204


class CoursesApi(Resource):

    def get(self):

        result = []
        course_id = request.args.get('course_id')

        if course_id:
            course_object = CourseModel.query.get(course_id)
            if course_object:
                for student in course_object.students:
                    result.append({'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name})
            else:
                abort(400, message=f'Wrong sourcery id {course_id}')
        else:
            abort(400, message='You Get What You Give')

        return {'data': result}, 200


api.add_resource(StudentsApi, '/students', '/students/<int:student_id>')
api.add_resource(StudentsCourses, '/students/<int:student_id>/courses/<int:course_id>',
                 '/students/<int:student_id>/courses')
api.add_resource(CoursesApi, '/courses')
