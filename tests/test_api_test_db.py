import pytest
import requests


@pytest.mark.parametrize('test_input, list_res',
                         [('/api/v1/students?students_number=4', b'[{"AA-00": 3}]\n'),
                          ('/api/v1/groups?group_name=AA-11',
                           b'["Student_0 Student_0", "Student_1 Student_1", "Student_2 Student_2", "Stude'
                           b'nt_3 Student_3", "Student_4 Student_4", "Student_5 Student_5"]\n'),
                          ('/api/v1/courses?course_name=course_name_1', b'[]\n')])
def test_get(client, db_create, test_input, list_res):
    response = client.get(test_input)
    assert response.status_code == 200
    assert response.data == list_res


@pytest.mark.parametrize('test_input',
                         ['/api/v1/students?students_not_number=4', '/api/v1/groups?group_not_name=AA-11',
                          '/api/v1/courses?course_not_name=course_name_1'])
def test_error_get(client, db_create, test_input):
    response = client.get(test_input)
    assert response.status_code == 400
    assert response.data == b'{"message": "You Get What You Give"}\n'


def test_delete(client, db_create):
    response = client.delete('http://127.0.0.1:5000/api/v1/students/5')
    assert response.status_code == 200
    assert response.data == b'"Good Kill. Number 5 is no more. 8 poor bastards to go"\n'
    response = client.delete('http://127.0.0.1:5000/api/v1/students/5')
    assert response.status_code == 404
    assert response.data == b'{"message": "Wrong target mark 5"}\n'


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_post(client, db_create, first_name, last_name):
    response = client.post('http://127.0.0.1:5000/api/v1/students',
                           json={'first_name': first_name, 'last_name': last_name})
    assert response.status_code == 201
    assert response.data == bytes(f'"New poor soul {first_name} {last_name} is condemned"\n', 'utf-8')


@pytest.mark.parametrize('first_name, last_name', [('Liolyk', 'Roundabout')])
def test_error_post(client, db_create, first_name, last_name):
    response = client.post('http://127.0.0.1:5000/api/v1/students',
                           json={'first_not_name': first_name, 'last_name': last_name})
    assert response.status_code == 400
    assert response.data == b'{"message": {"first_name": "Missing required parameter in the JSON body or the post body or the query string"}}\n'


def test_put(client, db_create):
    response = client.put('http://127.0.0.1:5000/api/v1/students/7',
                          json={'course_add': 1})
    assert response.status_code == 200
    assert response.data == b'"Poor soul Student_3 Student_3 now cursed with course_name_1"\n'
    response = client.put('http://127.0.0.1:5000/api/v1/students/7', json={'course_add': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n'


def test_error_put(client, db_create):
    response = client.put('http://127.0.0.1:5000/api/v1/students/7', json={'course_add': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already cursed with course_name_1"}\n'
    response = client.put('http://127.0.0.1:5000/api/v1/students/15',
                          json={'course_add': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Bastard is missing"}\n'


def test_put_remove(client, db_create):
    response = client.put('http://127.0.0.1:5000/api/v1/students/7', json={'course_remove': 1})
    assert response.status_code == 200
    assert response.data == b'"Poor soul Student_3 Student_3 will suffer course_name_1 no more"\n'


def test_error_put_remove(client, db_create):
    response = client.put('http://127.0.0.1:5000/api/v1/students/7', json={'course_remove': 1})
    assert response.status_code == 404
    assert response.data == b'{"message": "Poor soul Student_3 Student_3 already free from course_name_1"}\n'
    response = client.put('http://127.0.0.1:5000/api/v1/students/15', json={'course_remove': 1})
    assert response.status_code == 400
    assert response.data == b'{"message": "Bastard is missing"}\n'
