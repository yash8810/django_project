# Use official Python image as base
FROM python:3.10-slim
 
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
# Create app directory
WORKDIR /app
 
# Install system dependencies (Postgres client, build tools, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
&& rm -rf /var/lib/apt/lists/*
 
# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy project files
COPY . /app/
 
# Collect static files
RUN python manage.py collectstatic --noinput || true
 
# Run Gunicorn server
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]