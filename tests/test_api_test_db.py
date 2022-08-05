import pytest
from conftest import StudentModel, CourseModel


@pytest.mark.parametrize('test_input, list_res',
                         [('/api/v1/students?students_number=4', b'{"data": ["AA-00"]}\n'),
                          ('/api/v1/courses?course_name=course_name_1', b'{"data": []}\n')])
def test_get(client, db_create, test_input, list_res):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.data == list_res


@pytest.mark.parametrize('test_input',
                         ['/api/v1/students?students_not_number=4',
                          '/api/v1/courses?course_not_name=course_name_1'])
def test_error_get(client, db_create, test_input):
    response = client.get(test_input)
    assert response.status_code == 400
    assert response.data == b'{"message": "You Get What You Give"}\n'


@pytest.mark.parametrize('test_student_number, res_text', [(5, b''), (2055, b'')])
def test_delete(client, db_create, test_student_number, res_text):
    # students_count = StudentModel.query.count()
    response = client.delete('/api/v1/students/5')
    assert response.status_code == 204
    assert response.data == res_text
    # assert StudentModel.query.count() == students_count - 1
    assert StudentModel.query.filter_by(id=test_student_number).first() is None


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_post(client, db_create, first_name, last_name):
    students_count = StudentModel.query.count()
    response = client.post('/api/v1/students', json={'first_name': first_name, 'last_name': last_name})
    assert response.status_code == 201
    assert response.data == bytes(
        f'{{"data": {{"id": 10, "first_name": "{first_name}", "last_name": "{last_name}"}}}}\n',
        'utf-8')
    assert StudentModel.query.count() == students_count + 1
    assert StudentModel.query.filter_by(first_name=first_name, last_name=last_name).first() is not None


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_error_post(client, db_create, first_name, last_name):
    response = client.post('/api/v1/students', json={'first_not_name': first_name, 'last_name': last_name})
    assert response.status_code == 400
    assert response.data == b'{"message": {"first_name": "Missing required parameter in the JSON body or the post body or the query string"}}\n'
    response = client.post('/api/v1/students', json={'first_name': first_name, 'last_not_name': last_name})
    assert response.status_code == 400
    assert response.data == b'{"message": {"last_name": "Missing required parameter in the JSON body or the post body or the query string"}}\n'


@pytest.mark.parametrize('test_student_input,test_course_input, res_code, res_text', [(7, 1, 200,
                                                                                       b'{"data": {"id": 7, "first_name": "Student_3", "last_name": "Student_3", "courses": [1]}}\n'),
                                                                                      (7, 1, 400,
                                                                                       b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n')])
def test_put(client, db_create, test_student_input, test_course_input, res_code, res_text):
    response = client.put(f'http://127.0.0.1:5000/api/v1/students/{test_student_input}/courses',
                          json={'course': test_course_input})
    assert response.status_code == res_code
    assert response.data == res_text
    assert CourseModel.query.get(test_course_input) in StudentModel.query.get(test_student_input).courses


@pytest.mark.parametrize('test_student_input, test_course_input, test_param, res_code, res_text', [
    (7, 1, 'course', 400, b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n'),
    (15, 1, 'course', 404, b'{"message": "Bastard is missing"}\n'),
    (7, 11, 'course', 400, b'{"message": "Wrong sourcery number 11"}\n'),
    (7, 1, 'not_course', 400, b'{"message": "Be wise with your wishes"}\n')])
def test_error_put(client, db_create, test_student_input, test_course_input, test_param, res_code, res_text):
    response = client.put(f'/api/v1/students/{test_student_input}/courses', json={test_param: test_course_input})
    assert response.status_code == res_code
    assert response.data == res_text


@pytest.mark.parametrize('test_course_number, res_text', [(1, b''), (11, b'')])
def test_delete_course_from_student(client, db_create, test_course_number, res_text):
    response = client.delete('/api/v1/students/7/courses', json={'course': test_course_number})
    assert response.status_code == 204
    assert response.data == res_text
    assert CourseModel.query.get(test_course_number) not in StudentModel.query.get(7).courses


@pytest.mark.parametrize('test_student_input, test_course_input, test_param, res_code, res_text', [
    (7, 1, 'course', 404, b'{"message": "Poor soul Student_3 Student_3 already free from course_name_1"}\n'),
    (15, 1, 'course', 404, b'{"message": "Bastard is missing"}\n'),
    (7, 11, 'course', 404, b'{"message": "Wrong sourcery number 11"}\n'),
    (7, 1, 'not_course', 400, b'{"message": "Be wise with your wishes"}\n')])
def test_error_delete_course_from_student(client, db_create, test_student_input, test_course_input, test_param,
                                          res_code, res_text):
    response = client.delete(f'/api/v1/students/{test_student_input}/courses', json={test_param: test_course_input})
    assert response.status_code == res_code
    assert response.data == res_text
