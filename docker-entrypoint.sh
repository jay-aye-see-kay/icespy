#!/bin/bash
set -e

# Function to wait for database to be ready (for SQLite, just check if directory exists)
wait_for_db() {
    echo "Ensuring database directory exists..."
    mkdir -p /app/data
}

# Initialize database if needed
init_db() {
    echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput
    
    echo "Running database migrations..."
    uv run python manage.py migrate --noinput
    
    # Create superuser if environment variables are provided
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        uv run python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
EOF
    fi
}

# Main execution
wait_for_db
init_db

# Execute the main command
exec "$@"
