#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate --noinput

# test
python -Wa manage.py test --noinput

# selenium test


