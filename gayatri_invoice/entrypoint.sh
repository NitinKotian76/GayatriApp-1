#! /bin/bash
python manage.py collectstatic --no-input
gunicorn main.wsgi:application --bind 0.0.0.0:8000 &
# poetry run python3 manage.py runserver

wait
