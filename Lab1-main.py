from wsgiref.simple_server import make_server
from datetime import datetime
import json

from dateutil.parser import parse
from pytz import timezone, all_timezones
from tzlocal import get_localzone

local_tz = str(get_localzone())

response_parts = [
''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Time app</title>
</head>
<body>
''',
'''
</body>
</html>
'''
]

def get_ok_html(tz, time):
    return '200 OK',[
        response_parts[0],
        '<h2>Time: </h2>', time.strftime('%Y-%m-%d %H:%M:%S'),
        '<h3>Zone: </h3>', tz,
        response_parts[1]
    ]

def get_bad_html():
    return '400 BAD REQUEST', [
        response_parts[0],
        '<h2>400 BAD REQUEST</h2>',
        response_parts[1]
    ]

def get_ok_json(obj):
    return '200 OK', [json.dumps(obj)]

def get_bad_json():
    return '400 BAD REQUEST', '{ "error": "BAD REQUEST" }'

def time_app(environ, start_response):
    path = environ['PATH_INFO'][1:]
    method = environ['REQUEST_METHOD']
    
    #HTML
    if not path.startswith('api') and method == 'GET':
        headers = [('Content-type', 'text/html; charset=utf-8')]
        try:
            tz = path if path != '' else local_tz
            time = datetime.now(tz= timezone(tz))

            status, body = get_ok_html(tz, time)
        except:
            status, body = get_bad_html()

    #API
    elif path.startswith('api') and method == 'POST':
        headers = [('Content-type', 'application/json; charset=utf-8')]
        try:
            length = environ['CONTENT_LENGTH']
            length = 0 if not length else int(environ['CONTENT_LENGTH'] )
            body = json.loads(environ['wsgi.input'].read(length).decode('utf-8') or '{}')

            if path == 'api/v1/time':
                tz =  body['tz'] if 'tz' in body else local_tz
                time = datetime.now(tz= timezone(tz))

                status, body = get_ok_json({'tz': tz, 'time': time.strftime('%H:%M:%S')})
            

            elif path == 'api/v1/date':
                tz = body["tz"] if "tz" in body else local_tz
                time = datetime.now(tz= timezone(tz))

                status, body = get_ok_json({'tz': tz, 'date': time.strftime('%Y-%m-%d')})

            elif path == 'api/v1/datediff':
                tz = body['start']['tz'] if 'tz' in body['start'] else local_tz
                start = timezone(tz).localize(parse(body['start']['date']))

                tz = body['end']['tz'] if 'tz' in body['end'] else local_tz
                end = timezone(tz).localize(parse(body['end']['date'])) 

                diff = end - start

                status, body = get_ok_json({'diff': str(diff)})

            else:
                status, body = get_bad_json()
            
        except:
            status, body = get_bad_json()
 
    #Any else
    else:
        headers = [('Content-type', 'text/html; charset=utf-8')]
        status, body = get_bad_html()

    start_response(status, headers)
    return [x.encode() for x in body]


if __name__ == '__main__':
    # Запуск wsgi сервера
    httpd = make_server('', 8080, time_app)
    print("Serving on port 8080...")
    httpd.serve_forever()