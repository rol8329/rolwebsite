#!/bin/bash

# Exit on any error
set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h ${DB_HOST:-postgres} -p ${DB_PORT:-5432} -U ${DB_USER:-postgres}; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if it doesn't exist..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='rol8329',
        email='roland.le.goff@gmail.com',
        password='${DJANGO_SUPERUSER_PASSWORD:-changeme123}'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF

# Collect static files (if not done in Dockerfile)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django application
echo "Starting Django server..."
if [ "$ENVIRONMENT" = "PRODUCTION" ]; then
    exec gunicorn rolwebsite.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --worker-class gthread \
        --threads 2 \
        --worker-connections 1000 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 30 \
        --keep-alive 2 \
        --log-level info \
        --access-logfile /app/logs/access.log \
        --error-logfile /app/logs/error.log
else
    exec python manage.py runserver 0.0.0.0:8000
fi