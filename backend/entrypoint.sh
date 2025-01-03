#!/bin/bash

# Default to development environment
PROD=${PROD:-True}

echo "PROD is set to $PROD"

if [ $PROD == True ]; then
    echo "Starting Gunicorn server..."
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
    echo "Starting Django development server..."
    python manage.py runserver 0.0.0.0:8000
fi
