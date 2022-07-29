import requests
# res = requests.delete('http://127.0.0.1:5000/api/v1/students/41')
res = requests.get('http://127.0.0.1:5000/api/v1/students?students_number=18')
# res = requests.post('http://127.0.0.1:5000/api/v1/students', json={'first_name': 'Liolyk', 'last_name': 'Roundabout'})
# res = requests.put('http://127.0.0.1:5000/api/v1/students/1', json={'course_add': 1})
# res = requests.put('http://127.0.0.1:5000/api/v1/students/1', json={'course_remove': 1})
print(res, res.json(), res.status_code, res.request.method, res.headers['Content-Type'])

