echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 2
done
 
echo "PostgreSQL is ready!"
 
# Run migrations (creates tables from models.py)
python manage.py migrate --noinput
 
# Start Django server (Gunicorn recommended for production)
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3