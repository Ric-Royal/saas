#!/bin/sh

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z postgres 5432; do
  sleep 1
done

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start application
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 