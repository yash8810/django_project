#!/bin/sh
 
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 2
done
 
echo "PostgreSQL is ready!"
 
# Apply database migrations
python manage.py migrate --noinput
 
# Collect static files (for Django frontend assets)
python manage.py collectstatic --noinput

# Start Django server (Gunicorn recommended for production)
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3