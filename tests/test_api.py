import pytest
import requests


@pytest.mark.parametrize('test_input, list_res',
                         [('/api/v1/students?students_number=18', b'[{"ZY-52": 18}, {"TX-87": 18}]\n'),
                          ('/api/v1/groups?group_name=OF-40', ['Oleksander Lysenko',
                                                               'Mykhailo Boiko',
                                                               'Vadym Boiko',
                                                               'Mykola Tkachuk',
                                                               'Pylyp Melnyk',
                                                               'Georgiy Bondarenko',
                                                               'Oleksiy Petrenko',
                                                               'Marko Lysenko',
                                                               'Pavlo Olyinyk',
                                                               'Kyrylo Rudenko',
                                                               'Vasyl Lysenko',
                                                               'Georgiy Melnyk',
                                                               'Petro Koval',
                                                               'Pavlo Rudenko',
                                                               'Pylyp Olyinyk',
                                                               'Volodymyr Kovalenko',
                                                               'Pavlo Lysenko',
                                                               'Oleksiy Koval',
                                                               'Boryslav Koval'])])
def test_get2(client, test_input, list_res):
    response = client.get(test_input)
    assert response.status_code == 200
    # assert response.data == list_res
    # assert bytes_res2 in response.data
