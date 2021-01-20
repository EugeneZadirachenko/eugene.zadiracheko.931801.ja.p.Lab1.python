import requests
import json

from tzlocal import get_localzone

url = 'http://localhost:8080/'
local_tz = str(get_localzone())

result = []

try:
    response = requests.get(url)
    assert response.status_code == 200
    assert local_tz in response.text
except:
    result.append('1')
    
try:
    response = requests.get(url + 'UTC')
    assert response.status_code == 200
    assert 'UTC' in response.text
except:
    result.append('2')

try:
    response = requests.get(url + 'Europe/Moscow')
    assert response.status_code == 200
    assert 'Europe/Moscow' in response.text
except:
    result.append('3')

try:
    response = requests.post(url + 'api')
    assert response.status_code == 400
except:
    result.append('4')

try:
    response = requests.post(url + 'api/adss')
    assert response.status_code == 400
except:
    result.append('5')

try:
    response = requests.post(url + 'api/adss')
    assert response.status_code == 400
except:
    result.append('6')

try:
    response = requests.post(url + 'api/v1')
    assert response.status_code == 400
except:
    result.append('7')

try:
    response = requests.post(url + 'api/v1/time')
    assert response.status_code == 200
except:
    result.append('8')

try:
    response = requests.post(url + 'api/v1/time')
    assert response.status_code == 200
    obj = json.loads(response.text)
    assert obj['tz'] == local_tz
except:
    result.append('9')

try:
    response = requests.post(url + 'api/v1/time', data= json.dumps({'tz': 'UTC'}))
    assert response.status_code == 200
    obj = json.loads(response.text)
    assert obj['tz'] == 'UTC'
except:
    result.append('10')
try:
    response = requests.post(url + 'api/v1/time', data= json.dumps({'tz': 'Europe/Moscow'}))
    assert response.status_code == 200
    obj = json.loads(response.text)
    assert obj['tz'] == 'Europe/Moscow'
except:
    result.append('11')

try:
    response = requests.post(url + 'api/v1/time', data= json.dumps({'tz': 'UFO'}))
    assert response.status_code == 400
except:
    result.append('12')

try:
    response = requests.post(url + 'api/v1/date', data= json.dumps({'tz': 'Europe/Moscow'}))
    assert response.status_code == 200
    obj = json.loads(response.text)
    assert obj['tz'] == 'Europe/Moscow'
except:
    result.append('13')

try:
    response = requests.post(url + 'api/v1/datediff', data= json.dumps({
        'start': { 'date': '3:30pm 2020-12-01' },
        'end': { 'date': '12.20.2020 22:21:05', 'tz': 'UTC' }
    }))
    assert response.status_code == 200
    obj = json.loads(response.text)
except:
    result.append('14')

try:
    obj = {
        'begin': { 'date': '12:30pm 2020-12-01', 'timezone': local_tz },
        'end': { 'date': '12.20.2021 22:21:05', 'tz': 'UTC' }
    }
    response = requests.post(url + 'api/v1/datediff', data= json.dumps(obj))
    assert response.status_code == 400
except:
    result.append('15')

if not result:
    print('All tests passed successfully')
else:
    for x in result:
        print('Test ' + x + ' failed')