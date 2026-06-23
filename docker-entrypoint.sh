#!/bin/bash
set -e

# Handle modes
if [ "$1" = "rundev" ]; then
  echo "🚀 Starting Django development server on 0.0.0.0:8001"
  python manage.py runserver 0.0.0.0:8001
  exit 0
fi


if [ "$1" = "migrate" ]; then
  python manage.py migrate
  exit 0
fi

if [ "$1" = "makemigrations" ]; then
  python manage.py makemigrations
  exit 0
fi

# Default: run whatever was passed
exec "$@"
