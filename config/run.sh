#!/usr/bin/env bash

echo 'Waiting for Postgres...'
while ! nc -z ${POSTGRES_HOST} 5432; do
  sleep 0.1
done

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

echo " Run gunicorn"
gunicorn --workers=4 -b 0.0.0.0:5000 wsgi:app --reload