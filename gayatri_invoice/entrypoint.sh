#! /bin/bash
poetry run python manage.py collectstatic --no-input
poetry run gunicorn main.wsgi:application --bind 0.0.0.0:8000 &
# poetry run python3 manage.py runserver

wait
