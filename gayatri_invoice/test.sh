#!/bin/bash
set -e
cd /gayatri/gayatriapp
# Apply database migrations
python manage.py migrate --noinput

# test
python -Wa manage.py test --noinput

# selenium test


