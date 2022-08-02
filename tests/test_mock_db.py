import requests
from unittest.mock import Mock

def test_get_goups_by_number_of_students():

    get = Mock()
    StudentModel = Mock()

    # GroupModel.query.all()

    response = requests.get('http://127.0.0.1:5000/api/v1/students?students_number=18')
    assert response.status_code == 200
    get.assert_called()
    StudentModel.assert_not_called()
    # assert response.json() == 'list_res'