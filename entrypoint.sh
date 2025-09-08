#!/bin/sh
set -e  # exit if any command fails

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

echo "PostgreSQL is ready!"

# Apply database migrations
python manage.py makemigrations --noinput

python manage.py migrate --noinput
echo "Migrations applied!"

# Collect static files
python manage.py collectstatic --noinput
echo "Static files collected!"

# Create superuser if it doesn't exist
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created!")
else:
    print("Superuser already exists.")
EOF


# Start Gunicorn server
exec gunicorn gymer.wsgi:application --bind 0.0.0.0:8000 --workers 3
