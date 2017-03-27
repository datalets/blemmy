web: gunicorn publichealth.wsgi -b 0.0.0.0:$PORT -w 3 --log-file=-
init: python manage.py migrate
migrate: python manage.py migrate
