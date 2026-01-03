#!/bin/bash

set -e

cd /gayatri/gayatriapp
# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
python manage.py init_app

# Start Gunicorn
exec gunicorn main.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
