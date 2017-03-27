# web: uwsgi --http :$PORT --module=publichealth.wsgi:application --master --offload-threads 3
web: gunicorn publichealth.wsgi:application -b 0.0.0.0:$PORT -w 5 --log-file=-
init: python manage.py migrate
