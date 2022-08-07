import pytest
from conftest import StudentModel, CourseModel, db


@pytest.mark.parametrize('test_input, list_res', [('4', {"data": ["AA-00"]}), ('15', {"data": ["AA-11", "AA-00"]})])
def test_get_students_number(client, db_create, test_input, list_res):
    response = client.get(f'/api/v1/students?students_number={test_input}')
    assert response.status_code == 200
    assert response.json == list_res


@pytest.mark.parametrize('test_input, list_res', [('1', {"data": []})])
def test_get_courses(client, db_create, test_input, list_res):
    response = client.get(f'/api/v1/courses?course_id={test_input}')
    assert response.status_code == 200
    assert response.json == list_res


@pytest.mark.parametrize('test_input', [4])
def test_error_get_students_number(client, db_create, test_input):
    response = client.get(f'/api/v1/students?students_not_number={test_input}')
    assert response.status_code == 400
    assert response.json == {"message": "You Get What You Give"}


@pytest.mark.parametrize('test_input', [1])
def test_error_get_courses(client, db_create, test_input):
    response = client.get(f'/api/v1/courses?course_not_name=course_name_{test_input}')
    assert response.status_code == 400
    assert response.json == {"message": "You Get What You Give"}


@pytest.mark.parametrize('test_student_number, res_text', [(5, b''), (2055, b'')])
def test_delete(client, db_create, test_student_number, res_text):
    students_count = StudentModel.query.count() if StudentModel.query.get(test_student_number) else None

    response = client.delete('/api/v1/students/5')
    assert response.status_code == 204
    assert response.data == res_text
    if students_count:
        assert StudentModel.query.count() == students_count - 1
    assert StudentModel.query.get(test_student_number) is None


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_post(client, db_create, first_name, last_name):
    students_count = StudentModel.query.count()
    response = client.post('/api/v1/students', json={'first_name': first_name, 'last_name': last_name})
    assert response.status_code == 201
    assert response.json == {"data": {"id": 10, "first_name": first_name, "last_name": last_name}}
    assert StudentModel.query.count() == students_count + 1
    assert StudentModel.query.filter_by(first_name=first_name, last_name=last_name).first() is not None


@pytest.mark.parametrize('first_name_test_param, last_name_test_param, right_param',
                         [('first_name-not', 'last_name', 'first_name'), ('first_name', 'last_name-not', 'last_name')])
def test_error_post(client, db_create, first_name_test_param, last_name_test_param, right_param):
    response = client.post('/api/v1/students',
                           json={first_name_test_param: 'Liolyk', last_name_test_param: 'Roundabout'})
    assert response.status_code == 400
    assert response.json == {
        "message": {right_param: "Missing required parameter in the JSON body or the post body or the query string"}}


@pytest.mark.parametrize('test_student_input,test_course_input, res_text', [
    (7, 0, {"data": {"id": 7, "first_name": "Student_3", "last_name": "Student_3", "courses": [0]}}),
    (7, 1,
     {"data": {"id": 7, "first_name": "Student_3", "last_name": "Student_3", "courses": [0, 1]}}),
    (7, 1,
     {"data": {"id": 7, "first_name": "Student_3", "last_name": "Student_3", "courses": [0, 1]}})])
def test_put(client, db_create, test_student_input, test_course_input, res_text):
    response = client.put(f'/api/v1/students/{test_student_input}/courses',
                          json={'course': test_course_input})
    assert response.status_code == 200
    assert response.json == res_text
    assert CourseModel.query.get(test_course_input) in StudentModel.query.get(test_student_input).courses


@pytest.mark.parametrize('test_student_input, test_course_input, test_param, res_code, res_text', [
    (15, 1, 'course', 404, {"message": "Bastard is missing"}),
    (7, 11, 'course', 400, {"message": "Wrong sourcery number 11"}),
    (7, 1, 'not_course', 400, {"message": "Be wise with your wishes"})])
def test_error_put(client, db_create, test_student_input, test_course_input, test_param, res_code, res_text):
    response = client.put(f'/api/v1/students/{test_student_input}/courses', json={test_param: test_course_input})
    assert response.status_code == res_code
    assert response.json == res_text


@pytest.mark.parametrize('test_course_number', [0, 1, 11])
def test_delete_course_from_student(client, db_create, test_course_number):
    response = client.delete('/api/v1/students/7/courses', json={'course': test_course_number})
    assert response.status_code == 204
    assert response.data == b''
    assert CourseModel.query.get(test_course_number) not in StudentModel.query.get(7).courses


@pytest.mark.parametrize('test_student_input, test_course_input, test_param, res_code, res_text', [
    (15, 1, 'course', 404, {"message": "Bastard is missing"}),
    # (7, 11, 'course', 404, {"message": "Wrong sourcery number 11"}),
    (7, 1, 'not_course', 400, {"message": "Be wise with your wishes"})])
def test_error_delete_course_from_student(client, db_create, test_student_input, test_course_input, test_param,
                                          res_code, res_text):
    response = client.delete(f'/api/v1/students/{test_student_input}/courses', json={test_param: test_course_input})
    assert response.status_code == res_code
    assert response.json == res_text
