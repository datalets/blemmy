export COMPOSE_FILE=./docker-compose.yml
export COMPOSE_PROJECT_NAME=publichealth

default: build

build-cached:
	docker-compose build

build:
	docker-compose build --no-cache

run:
	docker-compose stop web	# for restart cases, when already running
	docker-compose up

run-detached:
	docker-compose up -d

django-restart-detached:
	docker-compose stop web
	docker-compose up -d web

stop:
	docker-compose stop

migrate:
	docker-compose exec web ./manage.py migrate

migrations:
	docker-compose exec web ./manage.py makemigrations

apply-migrations: migrations migrate

setup:
	docker-compose exec web ./manage.py migrate
	docker-compose exec web ./manage.py createsuperuser
	docker-compose exec web ./manage.py compress
	docker-compose exec web ./manage.py collectstatic

release:
	docker-compose build web
	docker-compose stop web
	docker-compose kill web
	docker-compose up -d web

django-exec-bash:
		# execute bash in the currently running container
	docker-compose exec web bash

django-run-bash:
	# run new django container, with bash, and remove it after usage
	docker-compose run --rm --no-deps web bash

django-shell:
	docker-compose exec web ./manage.py shell

logs:
	docker-compose logs -f --tail=500

django-backup:
	docker-compose exec web ./manage.py dumpdata --natural-foreign --indent=4 -e contenttypes -e auth.Permission -e sessions -e wagtailcore.pagerevision -e wagtailcore.groupcollectionpermission > ~/publichealth.home.json

backup-archive:
	gzip -1q ~/publichealth.home.json

backup: django-backup backup-archive

django-loaddata:
	gunzip ~/publichealth.home.json.gz
	docker-compose exec web ./manage.py loaddata ~/publichealth.home.json

restore: django-loaddata django-restart-detached

psql:
	docker-compose exec postgres psql -U postgres -d postgres

pg-run-detached:
	# start pg service
	docker-compose up -d postgres

pg-exec:
	docker-compose exec postgres bash

pg-dump:
	docker-compose exec postgres bash -c 'pg_dump -U postgres -d postgres -f ./dumps/latest.sql'

pg-restore:
	docker-compose exec postgres bash -c 'psql -U postgres -d postgres -f ./dumps/latest.sql'

pg-surefire-drop-restore-db:
	# drop existing database, recreate it, and then restore its content from backup.
	-docker-compose exec postgres bash -c 'dropdb -h localhost -U postgres postgres'
	docker-compose exec postgres bash -c 'createdb -h localhost -U postgres postgres'
	make pg-restore
