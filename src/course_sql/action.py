import requests
headers = {"Content-Type": "application/json; charset=utf-8"}
# res = requests.delete('http://127.0.0.1:5000/api/v1/group/45')
# res = requests.get('http://127.0.0.1:5000/api/v1/group?students_number=22')
res = requests.post('http://127.0.0.1:5000/api/v1/group', json={'first_name': 'Liolyk', 'last_name': 'Roundabout'})

print(res.json())