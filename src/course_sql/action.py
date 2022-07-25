import requests
# res = requests.delete('http://127.0.0.1:5000/api/v1/student/45')
# res = requests.get('http://127.0.0.1:5000/api/v1/student?students_number=22')
# res = requests.post('http://127.0.0.1:5000/api/v1/student', json={'first_name': 'Liolyk', 'last_name': 'Roundabout'})
# res = requests.put('http://127.0.0.1:5000/api/v1/student/1', json={'course': 1})
res = requests.put('http://127.0.0.1:5000/api/v1/student/1', json={'course_remove': 1})
print(res.json())