# web: uwsgi --http :$PORT --module=blemmy.wsgi:application --master --offload-threads 3
web: gunicorn blemmy.wsgi:application -b 0.0.0.0:$PORT -w 5 --log-file=-
init: python manage.py migrate
