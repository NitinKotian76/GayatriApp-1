#! /bin/bash

poetry run python manage.py collectstatic --no-input

poetry run gunicorn gayatriapp.wsgi:application --bind 0.0.0.0:8000 &

wait
