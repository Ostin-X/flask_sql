import pytest


@pytest.mark.parametrize('test_input, list_res',
                         [('/api/v1/students?students_number=4', b'{"data": [{"AA-00": 3}]}\n'),
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


def test_delete(client, db_create):
    response = client.delete('/api/v1/students/5')
    assert response.status_code == 204
    assert response.data == b''
    response = client.delete('http://127.0.0.1:5000/api/v1/students/5')
    assert response.status_code == 404
    assert response.data == b'{"message": "Bastard is missing"}\n'


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_post(client, db_create, first_name, last_name):
    response = client.post('/api/v1/students', json={'first_name': first_name, 'last_name': last_name})
    assert response.status_code == 201
    assert response.data == bytes(
        f'{{"data": {{"id": 10, "first_name": "{first_name}", "last_name": "{last_name}"}}}}\n',
        'utf-8')


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_error_post(client, db_create, first_name, last_name):
    response = client.post('/api/v1/students', json={'first_not_name': first_name, 'last_name': last_name})
    assert response.status_code == 400
    assert response.data == b'{"message": {"first_name": "Missing required parameter in the JSON body or the post body or the query string"}}\n'


def test_put(client, db_create):
    response = client.put('http://127.0.0.1:5000/api/v1/students/7/courses',
                          json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 200
    assert response.data == (b'{"data": {"id": 7, "first_name": "Student_3", "last_name": "Student_3", "courses": "c'
                             b'ourse_name_1"}}\n')
    response = client.put('http://127.0.0.1:5000/api/v1/students/7/courses',
                          json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n'


def test_error_put(client, db_create):
    response = client.put('/api/v1/students/7/courses', json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n'
    response = client.put('/api/v1/students/15/courses', json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Bastard is missing"}\n'
    response = client.put('/api/v1/students/7/courses', json={'first_name': '', 'last_name': '', 'course': 11})
    assert response.status_code == 404
    assert response.data == b'{"message": "Wrong sourcery number 11"}\n'
    response = client.put('/api/v1/students/7/courses', json={'first_name': '', 'last_name': '', 'not_course': 11})
    assert response.status_code == 400
    assert response.data == b'{"message": "Be wise with your wishes"}\n'

def test_delete_course_from_student(client, db_create):
    response = client.delete('/api/v1/students/7/courses', json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 204
    assert response.data == b''


def test_error_delete_course_from_student(client, db_create):
    response = client.delete('/api/v1/students/7/courses', json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 404
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already free from course_name_1"}\n'
    response = client.delete('/api/v1/students/15/courses', json={'first_name': '', 'last_name': '', 'course': 1})
    assert response.status_code == 404
    assert response.data == b'{"message": "Bastard is missing"}\n'
    response = client.delete('/api/v1/students/15/courses', json={'first_name': '', 'last_name': '', 'not_course': 1})
    assert response.status_code == 404
    assert response.data == b'{"message": "Bastard is missing"}\n'