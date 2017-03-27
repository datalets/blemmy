# web: uwsgi --http :$PORT --module=publichealth.wsgi:application --master --offload-threads 3
# web: gunicorn publichealth.wsgi -b 0.0.0.0:$PORT -w 5 --log-file=-
web: python manage.py runserver $PORT
init: python manage.py migrate
