Public Health Schweiz
=====================

Website of the Swiss Society for Public Health

## Development environment

Backend setup

```
sudo apt-get install python3-venv python3-dev libjpeg-dev
pyvenv env
. env/bin/activate

pip install -U pip
pip install -r requirements.txt

./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Frontend setup

```
npm install -g bower grunt-cli
npm install
bower install
grunt browser-sync
```
