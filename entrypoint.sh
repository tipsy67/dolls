#!/bin/sh
  echo "Running migrations..."
  python manage.py migrate

  echo "Collecting static files..."
  python manage.py collectstatic --noinput

#  echo "create custom superuser..."
#  python manage.py csu
#
#  echo "Load json data..."
#  python manage.py loaddata data.json

  echo "Load gunicorn..."
  gunicorn config.wsgi:application --bind 0.0.0.0:8000